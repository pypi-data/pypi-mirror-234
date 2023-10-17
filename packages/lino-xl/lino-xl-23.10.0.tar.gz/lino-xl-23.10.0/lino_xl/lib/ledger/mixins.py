# -*- coding: UTF-8 -*-
# Copyright 2008-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from django.db import models
from django.db.models import Q
from django.conf import settings

from etgen.html import E
from lino.utils import SumCollector
from lino.mixins import Sequenced
from lino.api import dd, rt, _
from lino.core import constants
from lino_xl.lib.contacts.mixins import PartnerRelated

from .choicelists import VoucherTypes, TradeTypes, VoucherStates
from .roles import LedgerUser

project_model = dd.get_plugin_setting('ledger', 'project_model', None)
has_payment_methods = dd.get_plugin_setting('ledger', 'has_payment_methods', False)


class ProjectRelated(dd.Model):
    class Meta:
        abstract = True

    project = dd.ForeignKey(
        project_model,
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_set_by_project")

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super().get_registrable_fields(site):
            yield f
        if project_model:
            yield 'project'


class PaymentRelated(PartnerRelated):
    class Meta:
        abstract = True

    payment_term = dd.ForeignKey(
        'ledger.PaymentTerm',
        related_name="%(app_label)s_%(class)s_set_by_payment_term",
        blank=True, null=True)

    if has_payment_methods:
        payment_method = dd.ForeignKey(
            'ledger.PaymentMethod',
            blank=True, null=True)
    else:
        payment_method = dd.DummyField(())

    def get_payment_term(self):
        return self.payment_term

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super().get_registrable_fields(site):
            yield f
        yield 'payment_term'

    def full_clean(self, *args, **kw):
        self.fill_defaults()
        super().full_clean(*args, **kw)

    def fill_defaults(self):
        if not self.payment_term and self.partner_id:
            self.payment_term = self.partner.payment_term
            if self.payment_term:
                self.payment_term_changed()
        if has_payment_methods:
            if not self.payment_method:
                self.payment_method = rt.models.ledger.PaymentMethod.objects.order_by('id').first()
                # self.payment_method = rt.models.ledger.PaymentMethod.objects.filter(
                #     Q(journal__isnull=True)|Q(journal=self.journal)).order_by('id').first()

    def payment_term_changed(self, ar=None):
        if self.payment_term:
            self.due_date = self.payment_term.get_due_date(self.entry_date)


class CashPayable(dd.Model):

    receivable_field = None

    class Meta:
        abstract = True



class Payable(dd.Model):
    class Meta:
        abstract = True

    your_ref = models.CharField(
        _("Your reference"), max_length=200, blank=True)
    due_date = models.DateField(_("Due date"), blank=True, null=True)
    # title = models.CharField(_("Description"), max_length=200, blank=True)

    def get_payment_term(self):
        return None

    def full_clean(self):
        if not self.due_date:
            payment_term = self.get_payment_term()
            if payment_term:
                self.due_date = payment_term.get_due_date(
                    self.voucher_date or self.entry_date)
        # super(Payable, self).full_clean()
        super().full_clean()

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super().get_registrable_fields(site):
            yield f
        yield 'your_ref'

    def get_due_date(self):
        return self.due_date or self.voucher_date

    def get_payable_sums_dict(self):
        raise NotImplemented()

    def get_movement_description(self, mvt, ar=None):
        for chunk in super().get_movement_description(mvt, ar):
            yield chunk
        if self.your_ref:
            yield self.your_ref

    def get_wanted_movements(self):
        if not self.journal.make_ledger_movements:
            return
        item_sums = self.get_payable_sums_dict()
        # logger.info("20120901 get_wanted_movements %s", sums_dict)
        counter_sums = SumCollector()
        partner = self.get_partner()
        has_vat = dd.is_installed('vat')
        kw = dict()
        for k, amount in item_sums.items():
            # amount = myround(amount)
            # first item of each tuple k is itself a tuple (account, ana_account)
            acc_tuple, prj, vat_class, vat_regime = k
            account, ana_account = acc_tuple
            # if not isinstance(acc_tuple, tuple):
            #     raise Exception("Not a tuple: {}".format(acc_tuple))
            if not isinstance(account, rt.models.ledger.Account):
                raise Exception("Not an account: {}".format(account))
            if has_vat:
                kw.update(
                    vat_class=vat_class, vat_regime=vat_regime)

            if account.needs_partner:
                kw.update(partner=partner)
            amount = self.journal.dc.normalized_amount(amount)
            yield self.create_ledger_movement(None, acc_tuple, prj, amount, **kw)
            counter_sums.collect(prj, amount)

        tt = self.get_trade_type()
        if tt is None:
            if len(counter_sums.items()):
                raise Warning("No trade type for {}".format(self))
            return
        acc = self.get_trade_type().get_main_account()
        if acc is None:
            if len(counter_sums.items()):
                raise Warning("No main account for {}".format(tt))
            return

        total_amount = 0
        for prj, amount in counter_sums.items():
            total_amount += amount
            yield self.create_ledger_movement(
                None, (acc, None), prj, -amount,
                partner=partner if acc.needs_partner else None,
                match=self.get_match())

        if dd.plugins.ledger.worker_model \
                and TradeTypes.clearings.main_account:
            payment_term = self.get_payment_term()
            if payment_term and payment_term.worker:
                # one movement to nullify the credit that was booked to the partner account,
                # another movment to book it to the worker's account:
                yield self.create_ledger_movement(
                    None, (acc, None), None, total_amount,
                    partner=partner, match=self.get_match())
                yield self.create_ledger_movement(
                    None, (TradeTypes.clearings.get_main_account(), None), None, -total_amount,
                    partner=payment_term.worker, match=self.get_match())


class Matching(dd.Model):
    class Meta:
        abstract = True

    match = dd.CharField(
        _("Match"), max_length=20, blank=True,
        help_text=_("The movement to be matched."))

    @classmethod
    def get_match_choices(cls, journal, partner, **fkw):
        """This is the general algorithm.
        """
        matchable_accounts = rt.models.ledger.Account.objects.filter(
            matchrule__journal=journal)
        fkw.update(account__in=matchable_accounts)
        fkw.update(cleared=False)
        if partner:
            fkw.update(partner=partner)
        qs = rt.models.ledger.Movement.objects.filter(**fkw)
        qs = qs.order_by('value_date')
        # qs = qs.distinct('match')
        return qs.values_list('match', flat=True)

    @dd.chooser(simple_values=True)
    def match_choices(cls, journal, partner):
        # todo: move this to implementing classes?
        return cls.get_match_choices(journal, partner)

    def get_match(self):
        # return self.match or self.get_default_match()
        return self.match or self  # 20191226


class VoucherItem(dd.Model):

    allow_cascaded_delete = ['voucher']

    class Meta:
        abstract = True

    # title = models.CharField(_("Description"), max_length=200, blank=True)

    def get_row_permission(self, ar, state, ba):
        """Items of registered invoices may not be edited

        """
        if not self.voucher_id:
            return False
        if not self.voucher.state.is_editable:
            if not ba.action.readonly:
                return False
        return super().get_row_permission(ar, state, ba)

    def get_ana_account(self):
        return None

class SequencedVoucherItem(Sequenced):

    class Meta:
        abstract = True

    def get_siblings(self):
        return self.voucher.items.all()

    def __str__(self):
        return str(self.voucher) + "#" + str(self.seqno)
        # return super().__str__()


class AccountVoucherItem(VoucherItem, SequencedVoucherItem):

    class Meta:
        abstract = True

    account = dd.ForeignKey(
        'ledger.Account',
        related_name="%(app_label)s_%(class)s_set_by_account")

    def get_base_account(self, tt):
        return self.account

    @dd.chooser()
    def account_choices(self, voucher):
        if voucher and voucher.journal:
            return voucher.journal.get_allowed_accounts()
        return rt.models.ledger.Account.objects.none()


# def set_partner_invoice_account(sender, instance=None, **kwargs):
#     if instance.account:
#         return
#     if not instance.voucher:
#         return
#     p = instance.voucher.partner
#     if not p:
#         return
#     tt = instance.voucher.get_trade_type()
#     instance.account = tt.get_partner_invoice_account(p)

# @dd.receiver(dd.post_analyze)
# def on_post_analyze(sender, **kw):
#     for m in rt.models_by_base(AccountVoucherItem):
#         dd.post_init.connect(set_partner_invoice_account, sender=m)



def JournalRef(**kw):
    # ~ kw.update(blank=True,null=True) # Django Ticket #12708
    kw.update(related_name="%(app_label)s_%(class)s_set_by_journal")
    return dd.ForeignKey('ledger.Journal', **kw)


def VoucherNumber(*args, **kwargs):
    return models.IntegerField(*args, **kwargs)


class PeriodRange(dd.Model):
    class Meta:
        abstract = True

    start_period = dd.ForeignKey(
        'ledger.AccountingPeriod',
        blank=True, verbose_name=_("Start period"),
        related_name="%(app_label)s_%(class)s_set_by_start_period")

    end_period = dd.ForeignKey(
        'ledger.AccountingPeriod',
        blank=True, null=True,
        verbose_name=_("End period"),
        related_name="%(app_label)s_%(class)s_set_by_end_period")


    def get_period_filter(self, voucher_prefix='', **kwargs):
        return rt.models.ledger.AccountingPeriod.get_period_filter(
            voucher_prefix, self.start_period, self.end_period, **kwargs)


class PeriodRangeObservable(dd.Model):
    class Meta:
        abstract = True

    observable_period_prefix = ''

    @classmethod
    def setup_parameters(cls, fields):
        fields.update(
            start_period=dd.ForeignKey(
                'ledger.AccountingPeriod',
                blank=True, null=True,
                help_text=_("Start of observed period range."),
                verbose_name=_("Period from")))
        fields.update(
            end_period=dd.ForeignKey(
                'ledger.AccountingPeriod',
                blank=True, null=True,
                help_text=_(
                    "Optional end of observed period range. "
                    "Leave empty to observe only the start period."),
                verbose_name=_("Period until")))
        super().setup_parameters(fields)

    @classmethod
    def get_request_queryset(cls, ar, **kwargs):
        pv = ar.param_values
        qs = super().get_request_queryset(ar, **kwargs)
        flt = rt.models.ledger.AccountingPeriod.get_period_filter(
            cls.observable_period_prefix, pv.start_period, pv.end_period)
        return qs.filter(**flt)

    @classmethod
    def get_title_tags(cls, ar):
        for t in super().get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.start_period is not None:
            if pv.end_period is None:
                yield str(pv.start_period)
            else:
                yield "{}..{}".format(pv.start_period, pv.end_period)


class ItemsByVoucher(dd.Table):
    label = _("Content")
    required_roles = dd.login_required(LedgerUser)
    master_key = 'voucher'
    order_by = ["seqno"]
    auto_fit_column_widths = True
    # display_mode = ((None, constants.DISPLAY_MODE_HTML),)
    preview_limit = 0


class MovementBase(PeriodRangeObservable):
    class Meta:
        abstract = True

    allow_cascaded_delete = ['voucher']
    observable_period_prefix = 'voucher__'
    product = None  # 20230617

    voucher = dd.ForeignKey(
        'ledger.Voucher',
        related_name="%(app_label)s_%(class)s_set_by_voucher")
    seqno = models.IntegerField(_("Seq.No."))
    partner = dd.ForeignKey(
        'contacts.Partner',
        related_name="%(app_label)s_%(class)s_set_by_partner",
        blank=True, null=True)
    value_date = models.DateField(_("Value date"), null=True, blank=True)
    match = models.CharField(_("Match"), blank=True, max_length=20)
    cleared = models.BooleanField(_("Cleared"), default=False)

    def select_text(self):
        v = self.voucher.get_mti_leaf()
        # v = self.voucher
        if v is None:
            return str(self.voucher)
        return "%s (%s)" % (v, v.entry_date)

    @dd.displayfield(
        _("Voucher"), sortable_by=[
            'voucher__journal__ref', 'voucher__accounting_period__year',
            'voucher__number'])
    def voucher_link(self, ar):
        if ar is None:
            return ''
        return ar.obj2html(self.voucher.get_mti_leaf())
        # return ar.obj2html(self.voucher)

    @dd.displayfield(_("Voucher partner"))
    def voucher_partner(self, ar):
        if ar is None:
            return ''
        voucher = self.voucher.get_mti_leaf()
        # voucher = self.voucher
        if voucher is None:
            return ''
        p = voucher.get_partner()
        if p is None:
            return ''
        return ar.obj2html(p)

    def __str__(self):
        return "%s.%d" % (str(self.voucher), self.seqno)

MovementBase.set_widget_options('voucher_link', width=12)
