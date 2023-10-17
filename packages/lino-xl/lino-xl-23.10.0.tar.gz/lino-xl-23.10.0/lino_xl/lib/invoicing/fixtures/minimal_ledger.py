# -*- coding: UTF-8 -*-
# Copyright 2012-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _
# from lino_xl.lib.ledger.choicelists import DC, CommonAccounts
from lino_xl.lib.invoicing.mixins import InvoicingAreas
# from django.utils.text import format_lazy

# vat = dd.resolve_app('vat')

def objects():
    return []
#     jnl = rt.models.ledger.Journal.objects.get(ref="SLS")
#     jnl.invoicing_area = InvoicingAreas.default
#     yield jnl

    # # FollowUpRule = rt.models.invoicing.FollowUpRule
    # JournalGroups = rt.models.ledger.JournalGroups
    # kw = dict(journal_group=JournalGroups.sales)
    # # MODEL = sales.InvoicesByJournal
    #
    # for ia in InvoicingAreas.get_list_items():
    #     if FollowUpRule.objects.filter(invoicing_area=ia).exists():
    #         # print("20221223 {} has already a followup rule".format(ia))
    #         continue
    #
    #     kw.update(trade_type='sales')
    #     kw.update(ref=ia.value, dc=DC.credit)
    #     kw.update(dd.str2kw('printed_name', _("Invoice")))
    #     # kw.update(dd.str2kw('name', _("Sales invoices")))
    #     # kw.update(printed_name=_("Invoice"))
    #     kw.update(dd.str2kw('name', format_lazy(_("{} invoices"), ia.text)))
    #     jnl = ia.journal_table.model.create_journal(**kw)
    #     yield jnl
    #     yield FollowUpRule(invoicing_area=ia, source_journal=jnl)
