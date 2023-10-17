# -*- coding: UTF-8 -*-
# Copyright 2016-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

try:
    import barcode
except ImportError:
    barcode = None

from django.db import models
from django.conf import settings
from lino.api import dd, _


class DeliveryUnits(dd.ChoiceList):
    verbose_name = _("Delivery unit")
    verbose_name_plural = _("Delivery units")

add = DeliveryUnits.add_item
add('10', _("Hour"), 'hour')
add('20', _("Piece"), 'piece')
add('30', _("Kg"), 'kg')


class ProductType(dd.Choice):
    table_name = 'products.Products'

class ProductTypes(dd.ChoiceList):
    item_class = ProductType
    verbose_name = _("Product type")
    verbose_name_plural = _("Product types")
    column_names = "value name text table_name *"

    @dd.virtualfield(models.CharField(_("Table name")))
    def table_name(cls, choice, ar):
        return choice.table_name

add = ProductTypes.add_item
add('100', _("Products"), 'default')


class PriceFactor(dd.Choice):
    field_cls = None
    def __init__(self, value, cls, name):
        self.field_cls = cls
        self.field_name = 'pf_' + name
        super().__init__(value, cls.verbose_name, name)

class PriceFactors(dd.ChoiceList):
    item_class = PriceFactor
    verbose_name = _("Price factor")
    verbose_name_plural = _("Price factors")




class BarcodeDriver(dd.Choice):
    barcode_length = None
    _current_demo_value = None

    def pop_demo_value(self):
        if self._current_demo_value is None:
            self._current_demo_value = "1" * self.barcode_length
        else:
            self._current_demo_value = str(int(self._current_demo_value)+1)
        return self._current_demo_value

    def write_svg_file(self, value):
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(value)
        ean.save(dd.plugins.products.barcodes_dir / value)



class EAN8Driver(BarcodeDriver):
    barcode_length = 8
    # value = "dummy"
    names = "ean8"

class EAN13Driver(BarcodeDriver):
    barcode_length = 13
    # value = "dummy"
    names = "ean13"


class BarcodeDrivers(dd.ChoiceList):
    verbose_name = _("Barcode driver")
    verbose_name_plural = _("Barcode drivers")

    # @classmethod
    # def on_analyze(cls, site):
    #     super().on_analyze(site)
    #     p = site.plugins.products
    #     drv = p.barcode_driver
    #     if drv is None:
    #         return
    #     if isinstance(drv, str):
    #         drv = cls.get_by_name(drv)
    #         p.barcode_driver = drv
    #     dd.inject_field(
    #         'products.Product', "barcode",
    #         models.CharField(max_length=drv.barcode_length,
    #             null=True, blank=True, unique=True))



add = BarcodeDrivers.add_item_instance
add(EAN8Driver())
add(EAN13Driver())


@dd.receiver(dd.pre_analyze)
def inject_barcode_field(sender, **kw):
    p = dd.plugins.products
    drv = p.barcode_driver
    if drv is None:
        dd.inject_field('products.Product', "barcode", dd.DummyField())
        return
    if isinstance(drv, str):
        drv = BarcodeDrivers.get_by_name(drv)
        p.barcode_driver = drv
    dd.inject_field(
        'products.Product', "barcode",
        models.CharField(max_length=drv.barcode_length,
            null=True, blank=True, unique=True))
