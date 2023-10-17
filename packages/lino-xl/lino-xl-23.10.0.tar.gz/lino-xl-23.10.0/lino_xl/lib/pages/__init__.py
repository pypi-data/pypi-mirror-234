# -*- coding: UTF-8 -*-
# Copyright 2012-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api.ad import Plugin, _


class Plugin(Plugin):

    verbose_name = _("Pages")
    ui_label = _("Pages")

    def post_site_startup(self, site):
        if site.is_installed("comments"):
            from lino_xl.lib.pages.choicelists import DataViewNodeType
            DataViewNodeType(site.models.comments.RecentComments).register()
        super().post_site_startup(site)

    def setup_main_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('pages.Nodes')

    def get_requirements(self, site):
        yield "python-lorem"
