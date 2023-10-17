# Copyright 2010-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Adds functionality for uploading files to the server and managing them.  See
:doc:`/specs/uploads`.


"""
from os.path import join
from lino import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Albums")
    menu_group = "office"
    needs_plugins = ['lino.modlib.uploads']

    remove_orphaned_files = False
    """
    Whether `checkdata --fix` should automatically delete orphaned files in the
    uploads folder.

    """

    def on_ui_init(self, kernel):
        super().on_ui_init(kernel)
        self.site.makedirs_if_missing(self.get_uploads_root())

    def get_uploads_root(self):
        # from django.conf import settings
        # return join(settings.SITE.MEDIA_ROOT, 'uploads')
        return join(self.site.django_settings['MEDIA_ROOT'], 'albums')

    # def setup_main_menu(self, site, user_type, m):
    #     mg = self.get_menu_group()
    #     m = m.add_menu(mg.app_label, mg.verbose_name)
    #     m.add_action('albums.MyFiles')

    def setup_config_menu(self, site, user_type, m):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('albums.Albums')

    # def setup_explorer_menu(self, site, user_type, m):
    #     mg = self.get_menu_group()
    #     m = m.add_menu(mg.app_label, mg.verbose_name)
    #     m.add_action('albums.AllFiles')
        # m.add_action('albums.FileUsages')
