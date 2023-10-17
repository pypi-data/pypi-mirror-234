# Copyright 2008-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Adds functionality for managing products.

See :doc:`/plugins/products`.

"""

from lino import ad, _


class Plugin(ad.Plugin):
    """The config descriptor for this plugin."""

    verbose_name = _("Products")
    needs_plugins = ['lino_xl.lib.xl']
    menu_group = 'products'
    price_selector = 'cal.EventType'
    barcode_driver = None
    barcodes_dir = None


    def on_initdb(self, site, verbosity=1):
    #     from lino_xl.lib.products.choicelists import BarcodeDrivers
    #     if isinstance(self.barcode_driver, str):
    #         self.barcode_driver = BarcodeDrivers.get_by_name(self.barcode_driver)
        if self.barcode_driver:
            self.barcodes_dir = site.media_root / "barcodes"
            self.barcodes_dir.mkdir(parents=True, exist_ok=True)
        super().on_initdb(site, verbosity=verbosity)

    def setup_config_menu(self, site, user_type, m):
        mg = self.get_menu_group()
        # if site.is_installed('sales'):
        #     mg = site.plugins.sales
        # else:
        #     mg = self
        m = m.add_menu(mg.app_label, mg.verbose_name)
        for pt in site.models.products.ProductTypes.get_list_items():
            m.add_action(pt.table_name, label=pt.text)
        # m.add_action('products.Products')
        m.add_action('products.Categories')

        # mg = site.plugins.sales
        # m2 = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('products.PriceRules')

    def setup_explorer_menu(self, site, user_type, m):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('products.PriceFactors')
        # m.add_action('products.ProductTypes')

    def get_requirements(self, site):
        if self.barcode_driver:
            yield "python-barcode"
