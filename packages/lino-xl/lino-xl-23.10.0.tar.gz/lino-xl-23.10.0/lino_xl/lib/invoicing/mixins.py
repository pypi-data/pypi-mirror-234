# -*- coding: UTF-8 -*-
# Copyright 2016-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from datetime import timedelta
from etgen.html import E, join_elems

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import format_lazy
from lino.api import dd, rt, _, gettext
from lino.core.gfks import gfk2lookup, GenericForeignKey, ContentType
from lino.modlib.gfks.fields import GenericForeignKeyIdField
from lino.utils import ONE_DAY
from lino.mixins.periods import rangefmt
from lino_xl.lib.ledger.utils import ZERO
from lino_xl.lib.cal.utils import day_and_month
from lino.modlib.system.choicelists import DurationUnits
from lino.modlib.summaries.mixins import Summarized
from lino_xl.lib.ledger.roles import LedgerUser, LedgerStaff
from lino_xl.lib.ledger.choicelists import VoucherTypes


MAX_SHOWN = 3  # maximum number of invoiced events shown in invoicing_info

class Periodicity(dd.Choice):
    renew_every = None
    renew_unit = None
    renew_before = None

    def __init__(self, value, text, renew_unit, renew_every, renew_before):
        super().__init__(value, text, value)
        self.renew_unit = renew_unit
        self.renew_every = renew_every
        self.renew_before = renew_before

class Periodicities(dd.ChoiceList):
    item_class = Periodicity
    verbose_name = _("Subscription periodicity")
    verbose_name_plural = _("Subscription periodicities")

add = Periodicities.add_item
add("m", _("Monthly"), DurationUnits.months, 1, 7)
add("q", _("Quarterly"), DurationUnits.months, 3, 14)
add("y", _("Yearly"), DurationUnits.years, 1, 28)


class InvoicingInfo(object):
    invoiced_qty = ZERO
    # invoiced_events = 0
    # used_events = []
    invoicings = None
    # sub_start = None
    # sub_end = None
    # invoicing_min_date = None
    # invoicing_max_date = None
    # tariff = None
    # 20210724
    invoiceable_product = None
    invoiceable_qty = None
    # asset_to_buy = None
    # number_of_events = None
    # min_asset = None
    # max_asset = None

    def __init__(self, enr, min_date, max_date):
        # print("20221223 InvoicingInfo() for {} ({}-{})".format(enr, min_date, max_date))
        self.generator = enr
        self.min_date = min_date
        self.max_date = max_date

        state_field = enr.target_invoicing_area.voucher_model._meta.get_field(
            'state')
        vstates = state_field.choicelist.get_editable_states()
        qs = enr.get_invoicings().exclude(voucher__state__in=vstates)
        product = enr.get_invoiceable_product(max_date)
        if product is not None:
            qs = qs.filter(product=product)
        self.invoicings = qs


        max_date = self.max_date or dd.today()
        end_date = enr.get_invoiceable_end_date()
        if end_date:
            max_date = min(max_date, end_date)

        # start_date = enr.get_invoiceable_start_date(max_date)
        # if not start_date:
        #     return

        self.invoiceable_qty = enr.get_invoiceable_qty()

        # sub = enr.get_invoicing_periodicity(product)
        # if sub is not None:
        #     raise Exception("20230625 This is now in subscriptions Period.get_invoice_items() and Subscription.compute_summary_values()")
        #     sub_start = start_date
        #     sub_end = sub.renew_unit.add_duration(sub_start, sub.renew_every) - ONE_DAY
        #     # print("20221223 subscription", rangefmt([sub_start, sub_end]))
        #     for i in self.invoicings:
        #         sub_start = sub_end + ONE_DAY
        #         sub_end = sub.renew_unit.add_duration(sub_start, sub.renew_every) - ONE_DAY
        #         # print("20221223 found existing invoicing until", sub_end)
        #     next_date = sub_start - timedelta(days=sub.renew_before)
        #     if min_date and next_date < min_date:
        #         # print("20221223 subscription is not yet started on", min_date)
        #         return
        #     if next_date > max_date:
        #         # print("20221223 no need to invoice renewal {} on {}".format(next_date, max_date))
        #         # next renewal date not yet reached
        #         return
        #     # self.invoiceable_product = product
        #     self.asset_to_buy = self.invoiceable_qty = 1
        #     self.sub_start = sub_start
        #     self.sub_end = sub_end
        #     self.invoiceable_product = product
        #     # print("20221223 renewal date reached", enr, self.invoiceable_qty, self.number_of_events, self.asset_to_buy)
        #     assert self.number_of_events is None and self.asset_to_buy is not None
        #     return

        # self.invoiced_events = enr.get_invoiceable_free_events() or 0
        # self.used_events = list(enr.get_invoiceable_events(
        #     start_date, max_date))

        # tariff = enr.get_invoicing_pass_type(product)
        # if tariff is not None:
        #     self.number_of_events = tariff.number_of_events
        #     self.min_asset = tariff.min_asset
        #     self.max_asset = tariff.max_asset

        for obj in self.invoicings:
            if obj.qty is not None:
                self.invoiced_qty += obj.qty
                # if self.number_of_events:
                #     self.invoiced_events += int(obj.qty * self.number_of_events)
        # print("20220507 invoiced, invoiceable qty", self.invoiced_qty, self.invoiceable_qty)

        # print("20181116 f %s", self.tariff.number_of_events)
        # if self.number_of_events:
        #     # this logic is now in Filler
        #     asset = self.invoiced_events - len(self.used_events)
        #     # dd.logger.info(
        #     #     "20220507 %s %s %s %s",
        #     #     start_date, max_date, asset, self.min_asset)
        #     if end_date and end_date < max_date and asset >= 0:
        #         # ticket #1040 : a participant who declared to stop before
        #         # their asset got negative should not get any invoice for
        #         # a next asset
        #         return
        #
        #     if self.min_asset is None:
        #         self.asset_to_buy = - asset
        #     elif asset > self.min_asset:
        #         return  # nothing to invoice
        #     else:
        #         self.asset_to_buy = self.min_asset - asset
        #
        #     if self.max_asset is not None:
        #         self.asset_to_buy = min(self.asset_to_buy, self.max_asset)

        # removed 20220507 because i don't see why it was:
        # elif self.invoiced_qty <= 0:
        #     self.asset_to_buy = 1
        if self.invoiceable_qty in (None, ''):
            return
        else:
            self.invoiceable_qty -= self.invoiced_qty
            if self.invoiceable_qty <= 0:
                return
            # self.asset_to_buy = self.invoiceable_qty - self.invoiced_qty
            # # print("20220507 self.asset_to_buy", self.asset_to_buy)
            # if self.asset_to_buy <= 0:
            #     return

        # qty = self.asset_to_buy * enr.get_invoiceable_qty()

        # 20210724
        self.invoiceable_product = product
        # self.invoiceable_qty = qty
        # self.asset_to_buy = asset_to_buy


    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self.__dict__)

    def format_as_html(self, ar):
        # return "20230701"
        if ar is None:
            elems = [str(obj.voucher) for obj in self.invoicings]
        else:
            elems = [ar.obj2html(obj.voucher) for obj in self.invoicings]
        # if len(self.used_events) == 0:
        #     return E.p(gettext("No invoiced events"))
        # # used_events = list(self.used_events)
        # invoiced = self.used_events[self.invoiced_events:]
        # coming = self.used_events[:self.invoiced_events]
        #
        # fmt = self.generator.get_invoiceable_event_formatter()
        # # def fmt(ev):
        # #     return self.generator.format_invoiceable_event(ev, ar)
        #
        # if len(invoiced) > 0:
        #     elems.append("{0} : ".format(_("Invoiced")))
        #     if len(invoiced) > MAX_SHOWN:
        #         elems.append("(...) ")
        #         invoiced = invoiced[-MAX_SHOWN:]
        #     elems += join_elems(map(fmt, invoiced), sep=', ')
        #     # s += ', '.join(map(fmt, invoiced))
        #     # elems.append(E.p(s))
        # if len(coming) > 0:
        #     if len(elems) > 0:
        #         elems.append(E.br())
        #     elems.append("{0} : ".format(_("Not invoiced")))
        #     elems += join_elems(map(fmt, coming), sep=', ')
        #     # s += ', '.join(map(fmt, coming))
        #     # elems.append(E.p(s))
        return E.p(*elems)

    def invoice_number(self, voucher):
        # used by lino_voga.courses.Course
        if self.invoicings is None:
            return 0
        n = 1
        for item in self.invoicings:
            n += 1
            if voucher and item.voucher.id == voucher.id:
                break
        # note that voucher.id is None when we are generating the
        # invoice, and then we return the next available number
        return n


class InvoicingArea(dd.Choice):
    # journal_table = None
    source_models = None
    voucher_model = 'sales.VatProductInvoice'
    item_model = 'sales.InvoiceItem'
    max_date_offset = -1
    today_offset = 0

    def __init__(self, value=None, text=None, names=None, source_models=None, **kwargs):
        super().__init__(value, text, names, **kwargs)
        if source_models:
            self.source_models = source_models

    def get_source_journals(self):
        for o in rt.models.invoicing.FollowUpRule.objects.filter(invoicing_area=self):
            yield o.source_journal

    def get_target_journal(self):
        # vtlist = [vt for vt in VoucherTypes.get_list_items()
        #     # if issubclass(vt.table_class, self.journal_table)]
        #     if issubclass(vt.model, dd.plugins.invoicing.voucher_model)]
        # return rt.models.ledger.Journal.objects.filter(voucher_type__in=vtlist)
        qs = rt.models.ledger.Journal.objects.filter(invoicing_area=self)
        if qs.count() > 1:
            tpl = "Multiple journals for invoicing area {} : {}"
            raise Exception(tpl.format(self, [j.ref for j in qs]))
        return qs.first()
        # return None


class InvoicingAreas(dd.ChoiceList):
    verbose_name = _("Invoicing area")
    verbose_name_plural = _("Invoicing areas")
    item_class = InvoicingArea
    column_names = 'value name text target_journal'
    required_roles = dd.login_required(LedgerStaff)
    max_length = 20

    # @dd.displayfield()
    # def target_journals(cls, choice, ar):
    #     return ", ".join([jnl.ref for jnl in choice.get_target_journals()])

    @dd.displayfield()
    def target_journal(cls, choice, ar):
        jnl = choice.get_target_journal()
        if jnl is None:
            return None
        return jnl.ref


# InvoicingAreas.add_item('invoicing', _("Invoicing"),  'default')


class InvoicingTargetVoucher(dd.Model):

    class Meta:
        abstract = True

    if dd.is_installed("invoicing"):
        invoicing_min_date = dd.DateField(_("Invoiceables from"), blank=True, null=True)
        invoicing_max_date = dd.DateField(_("until"), blank=True, null=True)

        def after_create_invoice(self):
            pass

    else:
        invoicing_min_date = dd.DummyField()
        invoicing_max_date = dd.DummyField()


class InvoicingTargetItem(dd.Model):

    class Meta:
        abstract = True

    title = models.CharField(_("Heading"), max_length=200, blank=True)

    if dd.is_installed("invoicing"):

        invoiceable_label = dd.plugins.invoicing.invoiceable_label

        invoiceable_type = dd.ForeignKey(
            ContentType,
            blank=True, null=True,
            verbose_name=format_lazy("{} {}", invoiceable_label, _('(type)')))
        invoiceable_id = GenericForeignKeyIdField(
            'invoiceable_type',
            blank=True, null=True,
            verbose_name=format_lazy("{} {}", invoiceable_label, _('(object)')))
        invoiceable = GenericForeignKey(
            'invoiceable_type', 'invoiceable_id',
            verbose_name=invoiceable_label)

        def discount_changed(self, ar=None):
            pass

        def get_amount(self):
            return 0

        @dd.chooser()
        def invoiceable_type_choices(cls):
            # show only invoiceable models when selecting an invoiceable_type
            return ContentType.objects.get_for_models(
                *rt.models_by_base(InvoiceGenerator)).values()

    else:
        invoiceable_type = dd.DummyField()
        invoiceable_id = dd.DummyField()
        invoiceable = dd.DummyField()


# class InvoiceGenerator(Summarized):
class InvoiceGenerator(dd.Model):

    class Meta:
        abstract = True

    # event_date_field = None
    _invoicing_info = None
    default_invoiceable_qty = 1
    target_invoicing_area = 'default'

    if dd.is_installed("invoicing"):
        # invoicings = GenericRelation(
        #     dd.plugins.invoicing.item_model,
        #     content_type_field='invoiceable_type',
        #     object_id_field='invoiceable_id')

        must_invoice = models.BooleanField(_("Must invoice"), default=True)

        @dd.displayfield(_("Invoicing info"))
        def invoicing_info(self, ar):
            # return "20230626"
            info = self.compute_invoicing_info(None, dd.today())
            return info.format_as_html(ar)

    # @classmethod
    # def on_analyze(cls, site):
    #     super(InvoiceGenerator, cls).on_analyze(site)
    #     de = cls.get_data_elem(cls.event_date_field)
    #     def func(self):
    #         return de.value_from_object(self)
    #     cls.get_invoiceable_event_date = func
    #     # if isinstance(cls.invoiceable_date_field, six.string_types):
    #     #     cls.invoiceable_date_field =

    # def get_invoicing_area(self):
    #     return None
    #     # return InvoicingAreas.delivered
    #     # raise NotImplementedError()
    #     # no longer overridden in Presto: return self.journal.room.invoicing_area
    #     # overridden in orders.Order

    def after_invoicing(self, ar=None):
        info = self.compute_invoicing_info(None, dd.today())
        if info.invoiceable_product is None:
            if self.must_invoice:
                self.must_invoice = False
                self.save()
        elif not self.must_invoice:
            self.must_invoice = True
            self.save()

    # def compute_summary_values(self):
        # ip = self.get_invoiceable_product()
        # iq = self.get_invoiceable_qty()
        # if iq is None or ip is None:
        #     self.must_invoice = False
        #     return
        # for i in self.get_invoicings():
        #     if i.qty is not None:
        #         if i.product == ip:
        #             iq -= i.qty
        # self.must_invoice = (iq > 0)


    # def get_summary_collectors(self):
    #     return []

    def get_invoicings(self, **kwargs):
        # deprecated? use invoicings instead?
        # item_model = dd.plugins.invoicing.item_model
        item_model = self.target_invoicing_area.item_model
        # item_model = rt.models.sales.InvoiceItem
        kwargs.update(gfk2lookup(item_model.invoiceable, self))
        return item_model.objects.filter(**kwargs)
        # assert not kwargs
        # return self.invoicings

    def get_last_invoicing(self):
        return self.get_invoicings().order_by('voucher__voucher_date').last()

    def allow_group_invoices(self):
        return True

    def get_invoice_items(self, info, invoice, ar):
        # print("20220507 get_invoice_items()", self,
        #     info.invoiceable_product, info.invoiceable_qty,
        #     info.number_of_events)
        # 20210724
        if info.invoiceable_product is None:
            return

        # invoiceable_qty = self.get_invoiceable_qty()
        if info.invoiceable_qty is None:
            return

        # 20210724
        kwargs = dict(product=info.invoiceable_product)
        # 20210804 kwargs = dict(invoiceable=self, product=info.invoiceable_product)
        # kwargs = dict(invoiceable=self)

        # if info.number_of_events is None:
        if True:
            # qty = asset_to_buy * info.invoiceable_qty
            qty = info.invoiceable_qty
            title = self.get_invoiceable_title()
            # if info.sub_start or info.sub_end:
            #     title += " " + rangefmt([info.sub_start, info.sub_end])
            kwargs.update(title=title, qty=qty)
            # print("20221224 gonna call add_voucher_item()", invoice.__class__,
            #     invoice.journal,
            #     invoice.journal.voucher_type.get_items_model())
            i = invoice.add_voucher_item(**kwargs)
            i.discount_changed(ar)
            yield i
            return

        # if info.sub_start or info.sub_end:
        #     raise Exception("What is a subscription with number_of_events?")
        #
        # asset_to_buy = info.asset_to_buy
        # if asset_to_buy is None:
        #     return
        #
        # # sell the asset in chunks
        #
        # number = info.invoiced_events // info.number_of_events
        # while asset_to_buy > 0:
        #     number += 1
        #     kwargs.update(
        #         title=self.get_invoiceable_title(number), qty=info.invoiceable_qty)
        #     i = invoice.add_voucher_item(**kwargs)
        #     i.discount_changed(ar)
        #     yield i
        #     asset_to_buy -= info.number_of_events

    def get_invoiceable_title(self, number=None):
        return str(self)

    def compute_invoicing_info(self, min_date, max_date):
        if self._invoicing_info is None \
           or self._invoicing_info.min_date != min_date \
           or self._invoicing_info.max_date != max_date:
            self._invoicing_info = InvoicingInfo(self, min_date, max_date)
        # assert self._invoicing_info.generator is self
        return self._invoicing_info

    def get_invoiceable_product(self, max_date=None):
        return None

    def get_invoiceable_qty(self):
        return self.default_invoiceable_qty

    # def get_invoicing_pass_type(self, product=None):
    #     if product is not None:
    #         return product.tariff
    #     return None

    def get_invoicing_periodicity(self, product):
        return

    def get_invoiceable_start_date(self, max_date):
        # don't look at events before this date.
        return None

    def get_invoiceable_end_date(self):
        # todo: return None here (but have existing children return self.end_date)
        return self.end_date

    def get_invoiceable_events(self, start_date, max_date):
        yield self

    def get_invoiceable_event_formatter(self):
        def fmt(ev, ar=None):
            txt = day_and_month(ev.start_date)
            if ar is None:
                return txt
            return ar.obj2html(ev, txt)
        return fmt

    def get_invoiceable_free_events(self):
        return 0

    # def get_invoiceable_amount(self, ie):
    #     return ie.amount

    # def get_invoiceable_event_date(self, ie):
    #     return ie.start_date

    # def get_invoiceable_amount(self):
    #     return None

    def get_invoiceable_partner(self):
        return None

    def get_invoiceable_payment_term(self):
        return None

    def get_invoiceable_paper_type(self):
        return None

    @classmethod
    def has_generators_for_plan(cls, plan, partner=None):
        if plan.invoicing_area != cls.target_invoicing_area:
            # print("20230515 target_invoicing_area", plan.invoicing_area.value, "is not for", cls)
            return False
        # if cls.target_invoicing_area is not None:
        #     if not plan.invoicing_area.value in cls.target_invoicing_area:
        #         # print("20230515", plan.invoicing_area.value, "is not for", cls)
        #         return False
        if plan.invoicing_area.source_models is not None:
            if not cls in plan.invoicing_area.source_models:
                # print("20230515", plan.invoicing_area.value, "is not for", cls,
                # "which is not in", plan.invoicing_area.source_models)
                return False
        return True

    @classmethod
    def get_generators_for_plan(cls, plan, partner=None):
        return cls.objects.all()

    # def setup_invoice_from_suggestion(self, invoice, plan, info):
    #     if info.invoicing_max_date is not None:
    #         invoice.invoicing_min_date = info.invoicing_min_date
    #         invoice.invoicing_max_date = info.invoicing_max_date
    #     else:
    #         invoice.invoicing_min_date = plan.min_date
    #         invoice.invoicing_max_date = plan.get_max_date()

    def setup_invoice_item(self, item):
        pass

    @classmethod
    def filter_by_invoice_recipient(cls, qs, partner, fieldname):
        q1 = models.Q(**{
            fieldname + '__salesrule__invoice_recipient__isnull': True,
            fieldname:partner})
        q2 = models.Q(**{
            fieldname+'__salesrule__invoice_recipient':partner})
        return qs.filter(models.Q(q1 | q2))
