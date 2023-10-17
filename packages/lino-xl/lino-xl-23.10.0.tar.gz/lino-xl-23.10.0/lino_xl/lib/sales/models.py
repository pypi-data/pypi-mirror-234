# -*- coding: UTF-8 -*-
# Copyright 2008-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models

from lino.api import dd, rt, _
from etgen.html import E
from lino.utils.mldbc.mixins import BabelNamed
# from lino.mixins.periods import DateRange

from lino_xl.lib.ledger.mixins import Matching, SequencedVoucherItem, CashPayable
from lino_xl.lib.ledger.models import Voucher
from lino_xl.lib.ledger.choicelists import TradeTypes
from lino_xl.lib.invoicing.mixins import InvoiceGenerator
from lino_xl.lib.invoicing.mixins import InvoicingTargetVoucher, InvoicingTargetItem
from lino_xl.lib.storage.mixins import StorageTransferer
from lino_xl.lib.invoicing.mixins import InvoicingAreas
from .mixins import SalesDocument, ProductDocItem

has_payment_methods = dd.get_plugin_setting('ledger', 'has_payment_methods', False)

TradeTypes.sales.update(
    price_field_name='sales_price',
    price_field_label=_("Sales price"),
    base_account_field_name='sales_account',
    base_account_field_label=_("Sales account"))


class PaperType(BabelNamed):

    templates_group = 'sales/VatProductInvoice'

    class Meta:
        app_label = 'sales'
        abstract = dd.is_abstract_model(__name__, 'PaperType')
        verbose_name = _("Paper type")
        verbose_name_plural = _("Paper types")

    template = models.CharField(_("Template"), max_length=200, blank=True)

    @dd.chooser(simple_values=True)
    def template_choices(cls):
        bm = rt.models.printing.BuildMethods.get_system_default()
        return rt.find_template_config_files(
            bm.template_ext, cls.templates_group)

class VatProductInvoice(SalesDocument, Matching, InvoicingTargetVoucher,
        StorageTransferer):
    # edit_totals = True
    quick_search_fields = "partner__name subject"

    class Meta:
        app_label = 'sales'
        abstract = dd.is_abstract_model(__name__, 'VatProductInvoice')
        verbose_name = _("Sales invoice")
        verbose_name_plural = _("Sales invoices")

    # show_items = dd.ShowSlaveTable('sales.ItemsByInvoice')

    # make_copy = MakeCopy()

    # def register_voucher(self, ar=None, do_clear=None):
    #     super().register_voucher(ar, do_clear)
    #     if self.payment_method is None:
    #         self.payment_method = self.get_default_payment_method(ar)

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super().get_registrable_fields(site):
            yield f
        yield 'due_date'
        yield 'voucher_date'
        yield 'entry_date'
        yield 'user'
        # yield 'item_vat'

    def get_print_items(self, ar):
        dv = rt.models.resolve(dd.plugins.sales.print_items_table)
        return dv.request(self)

    @dd.virtualfield(dd.PriceField(_("Balance to pay")))
    def balance_to_pay(self, ar):
        Movement = rt.models.ledger.Movement
        qs = Movement.objects.filter(
            partner=self.get_partner(),
            cleared=False,
            match=self.get_match())
        return Movement.get_balance(self.journal.dc.opposite(), qs)

    @dd.virtualfield(dd.PriceField(_("Balance before")))
    def balance_before(self, ar):
        Movement = rt.models.ledger.Movement
        qs = Movement.objects.filter(
            partner=self.get_partner(),
            cleared=False,
            value_date__lte=self.entry_date)
        qs = qs.exclude(voucher=self)
        return Movement.get_balance(self.journal.dc.opposite(), qs)


if has_payment_methods:

    class StartNewSale(dd.Action):
        label = _("Start new sale")
        show_in_toolbar = False

        def get_action_permission(self, ar, obj, state):
            if ar.get_user().sales_journal is None:
                return False
            return super().get_action_permission(ar, obj, state)

        def run_from_ui(self, ar):
            journal = ar.get_user().sales_journal
            instance = journal.voucher_type.table_class.create_instance(
                ar,
                journal=journal,
                partner=journal.partner)
            instance.full_clean()
            instance.save_new_instance(ar)
            ar.goto_instance(instance)


    class CashInvoice(VatProductInvoice):

        class Meta:
            app_label = 'sales'
            abstract = dd.is_abstract_model(__name__, 'CashInvoice')
            verbose_name = _("Cash invoice")
            verbose_name_plural = _("Cash invoices")

        cash_received = dd.PriceField(_("Cash received"), blank=True, null=True)
        cash_returned = dd.PriceField(_("Cash returned"), blank=True, null=True)

        start_new_sale = StartNewSale()

        def cash_received_changed(self, ar):
            self.cash_returned = self.cash_received - self.total_incl

        @dd.displayfield(_("Cash to return"))
        def cash_to_return(self, ar):
            if self.payment_method.is_cash:
                if self.total_incl and self.cash_received:
                    if self.cash_received >= self.total_incl:
                        return self.cash_received - self.total_incl

        # def get_payable_sums_dict(self):
        def get_wanted_movements(self):
            for mvt in super().get_wanted_movements():
                yield mvt
            if self.payment_method.payment_account is None:
                return
            if self.payment_method.is_cash:
                amount = self.cash_received - self.cash_returned
            else:
                amount = self.total_incl
            tt = self.get_trade_type()
            if self.partner is None:
                acc = tt.get_base_account()
            else:
                acc = tt.get_main_account()
                # acc = tt.get_partner_invoice_account(self.partner)
            if acc is None:
                raise Exception("20220706 acc is None {} {}".format(self.partner, tt))
            prj = None
            yield self.create_ledger_movement(
                None, (acc, None), prj, amount,
                partner=self.partner, match=self.get_match())
            yield self.create_ledger_movement(
                None, (self.payment_method.payment_account, None), prj, -amount,
                partner=self.partner, match=self.get_match())

            # sums_dict.collect(
            #     ((acc, None), self.project, None, None),
            #     cash_amount)
            #     sums_dict.collect(
            #         ((self.payment_method.payment_account, None), self.project, None, None),
            #         -amount)
            # return sums_dict


    dd.inject_field('users.User', 'sales_journal', dd.ForeignKey(
        'ledger.Journal', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_("Sales journal")
    ))

else:
    dd.inject_field('users.User', 'sales_journal', dd.DummyField())


class InvoiceItem(ProductDocItem, SequencedVoucherItem, InvoiceGenerator,
        InvoicingTargetItem):
    class Meta:
        app_label = 'sales'
        abstract = dd.is_abstract_model(__name__, 'InvoiceItem')
        verbose_name = _("Sales invoice item")
        verbose_name_plural = _("Sales invoice items")

    voucher = dd.ForeignKey(
        'sales.VatProductInvoice', related_name='items')
    # ship_ref = models.CharField(
    #     _("Shipment reference"), max_length=200, blank=True)
    # ship_date = models.DateField(_("Shipment date"), blank=True, null=True)

    master_data_fields = {'total_incl', 'total_base'}

    @classmethod
    def get_partner_filter_field(cls, partner):
        return "voucher__" + VatProductInvoice.get_partner_filter_field(partner)

    def get_master_data(self, ar, master_instance=None):
        if ar.master_instance.edit_totals:
            ar.master_instance.compute_totals()
        ar.master_instance.full_clean()
        ar.master_instance.save()
        return super().get_master_data(ar)

    @classmethod
    def get_generators_for_plan(cls, plan, partner=None):
        jnls = set(plan.invoicing_area.get_source_journals())
        if len(jnls) == 0:
            return []

        # jnls = [o.source_journal
        #     for o in rt.models.invoicing.FollowUpRule.objects.filter(
        #         source_journal=plan.invoicing_area.source_journal)]
        # jnls = [o.source_journal
        #     for o in rt.models.invoicing.FollowUpRule.objects.filter(
        #         invoicing_area=plan.invoicing_area)]
        # qs = cls.objects.filter(voucher__journal__in=plan.invoicing_area.get_source_journals())
        qs = cls.objects.filter(voucher__journal__in=jnls)
        if partner is not None:
            # qs = qs.filter(voucher__partner=partner)
            fldname = cls.get_partner_filter_field(partner)
            qs = cls.filter_by_invoice_recipient(qs, partner, fldname)
        return qs

        # trs = rt.models.invoicing.FollowUpRule.objects.filter(
        #     source_journal=plan.area.journal)
        # if trs.exist():
        # jnls = []
        # for tr in trs:
        #     trs = trs.filter(from_state=)
        #     tr.from_state
        #     qs = cls.objects.filter(voucher__journal__in=jnls)
        #     yield qs

    def get_invoiceable_product(self, max_date=None):
        return self.product

    def get_invoiceable_qty(self):
        return self.qty

    def get_invoiceable_title(self, number=None):
        return self.title

    def get_invoiceable_end_date(self):
        return None

    # def get_invoiceable_start_date(self, max_date):
    #     # don't look at events before this date.
    #     return None
    #
    def get_invoiceable_events(self, start_date, max_date):
        return []

    def get_invoiceable_free_events(self):
        return 0

    def get_invoiceable_partner(self):
        return self.voucher.partner

    def get_invoiceable_payment_term(self):
        return None

    def get_invoiceable_paper_type(self):
        return None

    # def setup_invoice_from_suggestion(self, invoice, plan, info):
    #     if info.invoicing_max_date is not None:
    #         invoice.invoicing_min_date = info.invoicing_min_date
    #         invoice.invoicing_max_date = info.invoicing_max_date
    #     else:
    #         invoice.invoicing_min_date = plan.min_date
    #         invoice.invoicing_max_date = plan.get_max_date()

    def setup_invoice_item(self, item):
        pass

InvoicingAreas.add_item('sales', _("Invoicing"), 'default',
    voucher_model=VatProductInvoice, voucher_item=InvoiceItem)

from .ui import *
