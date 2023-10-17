# -*- coding: UTF-8 -*-
# Copyright 2016-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Adds functionality for **invoicing**, i.e. automatically generating
invoices from data in the database.

See :doc:`/plugins/invoicing`.

"""

from lino.api.ad import Plugin, _
from django.utils.text import format_lazy
from django.utils.module_loading import import_string


class Plugin(Plugin):

    verbose_name = _("Invoicing")

    # needs_plugins = ['lino_xl.lib.ledger']
    needs_plugins = ['lino_xl.lib.sales']

    order_model = None

    # default_voucher_view = 'lino_xl.lib.sales.ui.InvoicesByJournal'
    voucher_type = 'sales.InvoicesByJournal'
    # voucher_model = 'sales.VatProductInvoice'
    # item_model = 'sales.InvoiceItem'

    invoiceable_label = _("Invoiced object")

    three_demo_areas = True
    """
    Whether the :fixture:`demo` fixture should generate three invoicing areas
    instead of one.
    """

    # delivery_notes_demo = False
    # """
    # Whether the :fixture:`demo` fixtures should generate delivery notes.
    # """

    def before_analyze(self):
        # print("20210722 before_analyze()")
        from lino.core.utils import resolve_model
        # self.voucher_model = resolve_model(self.voucher_model)
        # self.item_model = resolve_model(self.item_model)
        # ivm = self.item_model._meta.get_field('voucher').remote_field.model
        # if self.voucher_model != ivm:
        #     raise Exception("voucher_model is {} but should be {}".format(
        #         self.voucher_model, ivm))
        # assert issubclass(self.default_voucher_view, dbtables.Table)

        if self.order_model is not None:
            self.order_model = resolve_model(self.order_model)

    def post_site_startup(self, site):
        super().post_site_startup(site)
        from lino.core.utils import models_by_base, resolve_model
        from lino_xl.lib.invoicing.mixins import InvoiceGenerator
        from lino_xl.lib.invoicing.mixins import InvoicingAreas
        for ia in InvoicingAreas.get_list_items():
            ia.voucher_model = resolve_model(ia.voucher_model)
            ia.item_model = resolve_model(ia.item_model)
        for m in models_by_base(InvoiceGenerator):
            k = m.target_invoicing_area
            if isinstance(k, str):
                k = InvoicingAreas.get_by_name(k)
                if k is None:
                    raise Warning(
                        "Invalid value '{}' for {}.target_invoicing_area".format(
                            m.target_invoicing_area, m))
                m.target_invoicing_area = k
                # print("20230515", m, m.target_invoicing_area)
                # for k in m.target_invoicing_area:
                #     if not site.models.invoicing.InvoicingAreas.get_by_value(k):
                #         raise Warning(
                #             "Invalid name '{}' in {}.target_invoicing_area".format(
                #                 k, m))

        #     for jnl in ia.get_source_journals():
        #         if not issubclass(jnl.voucher_type.model, self.voucher_model):
        #             raise Warning("20221223 {} is not a {}".format(jnl.voucher_type.model, self.voucher_model))



    # def on_ui_init(self, kernel):
    #     if type(self.voucher_type) == str:
    #         VoucherTypes = self.site.models.ledger.VoucherTypes
    #         self.voucher_type = VoucherTypes.get_by_value(self.voucher_type)
    #     assert self.voucher_type.model is self.voucher_model
    #     assert self.voucher_type.get_items_model() is self.item_model

    def setup_main_menu(config, site, user_type, m):
        mg = site.plugins.sales
        m = m.add_menu(mg.app_label, mg.verbose_name)
        # m.add_action('invoicing.Plan', action='start_plan')
        for ia in site.models.invoicing.InvoicingAreas.get_list_items():
            if ia.get_target_journal() is None:
                # print("20230514 no target journals for", ia)
                continue
            # # m.add_instance_action(obj, action='start_invoicing')
            # m.add_action(obj, action='start_invoicing')
            m.add_action(
                'invoicing.PlansByArea', 'start_invoicing',
                # label=format_lazy(_("Create invoices {}"), obj),
                label=format_lazy(_("Start {}"), ia.text),
                params=dict(master_instance=ia))

    def setup_config_menu(self, site, user_type, m):
        mg = site.plugins.sales
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('invoicing.Tariffs')
        m.add_action('invoicing.FollowUpRules')

    def setup_explorer_menu(self, site, user_type, m):
        mg = site.plugins.sales
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('invoicing.AllPlans')
        m.add_action('invoicing.SalesRules')
        m.add_action('invoicing.InvoicingAreas')
