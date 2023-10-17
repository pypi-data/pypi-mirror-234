# -*- coding: UTF-8 -*-
# Copyright 2016-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from lino.api import dd, rt, _
from lino.modlib.users.mixins import StartPlan
from .mixins import InvoicingAreas


class StartInvoicing(StartPlan):
    label = _("Generate invoices")
    icon_name = 'basket'

    def get_plan_model(self, ar):
        return rt.models.invoicing.Plan


class StartInvoicingByArea(StartInvoicing):
    show_in_toolbar = True

    def get_plan_options(self, ar):
        mi = ar.master_instance
        # assert isinstance(mi, rt.models.invoicing.Area)
        return dict(
            invoicing_area=mi, partner=None)
            # target_journal=mi.get_target_journal())


class StartInvoicingForPartner(StartInvoicing):
    show_in_toolbar = True
    select_rows = True
    update_after_start = True

    def get_plan_options(self, ar):
        partner = ar.selected_rows[0]
        assert isinstance(partner, rt.models.contacts.Partner)
        return dict(partner=partner)


class StartInvoicingForOrder(StartInvoicing):
    show_in_toolbar = True
    select_rows = True
    update_after_start = True

    def get_plan_options(self, ar):
        order = ar.selected_rows[0]
        assert isinstance(order, dd.plugins.invoicing.order_model)
        return dict(order=order, partner=None, invoicing_area=InvoicingAreas.default)
        # return dict(order=order, partner=None)
        # return dict(order=order, partner=None, invoicing_area=order.get_invoicing_area())
        # return dict(order=order, partner=None, area=order.journal.room.invoicing_area)


class ExecutePlan(dd.Action):
    label = _("Execute plan")
    icon_name = 'money'
    sort_index = 54

    def run_from_ui(self, ar, **kw):
        plan = ar.selected_rows[0]
        for item in plan.items.filter(selected=True, invoice__isnull=True):
            item.create_invoice(ar)
        ar.success(refresh=True)


class ExecuteItem(ExecutePlan):
    label = _("Execute item")
    show_in_workflow = True
    show_in_toolbar = False


    def get_action_permission(self, ar, obj, state):
        if obj.invoice_id:
            return False
        return super(ExecuteItem, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        for item in ar.selected_rows:
            if item.invoice_id:
                raise Warning(
                    _("Invoice {} was already generated").format(
                        item.invoice))
            item.create_invoice(ar)
        ar.success(refresh=True)


class ToggleSelection(dd.Action):
    label = _("Toggle selections")

    def run_from_ui(self, ar, **kw):
        plan = ar.selected_rows[0]
        for item in plan.items.all():
            item.selected = not item.selected
            item.save()
        ar.success(refresh=True)
