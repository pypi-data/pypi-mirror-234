# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import logging ; logger = logging.getLogger(__name__)

import os
import io
from copy import copy

from django.conf import settings
from django.utils import translation
from etgen.html import tostring


try:
    from django.template import TemplateDoesNotExist
except ImportError:
    from django.template.loader import TemplateDoesNotExist

from django.template.loader import select_template

from lino.core.choicelists import ChoiceList, Choice
from lino.utils.media import MediaFile
from lino.api import rt, _


class NodeType(Choice):

    def register(self):
        NodeTypes.add_item_instance(self)

    def get_dynamic_story(self, ar, obj):
        return ""


class DataViewNodeType(NodeType):

    data_view = None

    def __init__(self, data_view, *args, **kwargs):
        self.data_view = data_view
        super().__init__(str(data_view), *args, **kwargs)

    def get_dynamic_story(self, ar, obj, **kwargs):
        dv = self.data_view
        sar = dv.request(parent=ar, limit=dv.preview_limit)
        # print("20230409", ar.renderer)
        txt = ''
        # rv += "20230325 [show {}]".format(dv)
        for e in sar.renderer.table2story(sar, **kwargs):
            txt += tostring(e)
        return txt

    def get_dynamic_paragraph(self, ar, obj, **kwargs):
        dv = self.data_view
        # sar = dv.request(parent=ar, limit=dv.preview_limit)
        sar = dv.request(parent=ar)
        return " / ".join([sar.obj2htmls(row) for row in sar])


class NodeTypes(ChoiceList):
    # verbose_name = _("Build method")
    verbose_name = _("Node type")
    verbose_name_plural = _("Node types")
    item_class = NodeType
    # app_label = 'lino'
    max_length = 50
