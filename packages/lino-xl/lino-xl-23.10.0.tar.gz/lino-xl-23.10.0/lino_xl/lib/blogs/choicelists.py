# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from django.db import models

class EntryStates(dd.Workflow):
    # verbose_name_plural = _("Enrolment states")
    required_roles = dd.login_required(dd.SiteAdmin)
    is_public = models.BooleanField(_("Public"), default=False)

    @classmethod
    def get_column_names(self, ar):
        return "value name text button_text is_public"

add = EntryStates.add_item
add('10', _("Draft"), 'draft', is_public=False)
add('20', _("Ready"), 'ready', is_public=False)
add('30', _("Public"), 'published', is_public=True)
add('40', _("Cancelled"), 'cancelled', is_public=False)
