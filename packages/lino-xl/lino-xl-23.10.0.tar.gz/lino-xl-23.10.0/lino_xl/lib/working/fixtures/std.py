# -*- coding: UTF-8 -*-
# Copyright 2016-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import rt, dd, _


def objects():
    SessionType = rt.models.working.SessionType
    yield SessionType(id=1, name="Default")

    # ServiceReport = rt.models.working.ServiceReport
    # ExcerptType = rt.models.excerpts.ExcerptType
    # kw = dict(
    #     build_method='weasy2html',
    #     # template='service_report.weasy.html',
    #     # body_template='default.body.html',
    #     # print_recipient=False,
    #     primary=True, certifying=True)
    # kw.update(dd.str2kw('name', ServiceReport._meta.verbose_name))
    # yield ExcerptType.update_for_model(ServiceReport, **kw)

    Product = rt.models.products.Product
    PriceRule = rt.models.products.PriceRule
    kw = dict(sales_price="69.90", storage_management=True)
    kw.update(dd.str2kw('name', _("Development")))
    kw.update(delivery_unit="hour")
    # kw.update(ref="dev", delivery_unit="hour")
    obj = Product(**kw)
    yield obj
    yield PriceRule(product=obj)
