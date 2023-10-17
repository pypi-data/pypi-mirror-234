# -*- coding: UTF-8 -*-
# Copyright 2008-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
from os.path import join, exists
import glob
from pathlib import Path
from datetime import datetime

from django.db import models
from django.db.models.fields.files import FieldFile
from django.conf import settings
from django.utils.text import format_lazy
# from lino.api import string_concat
from django.utils.translation import pgettext_lazy as pgettext
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError

from etgen.html import E, join_elems, tostring
from lino.api import dd, rt, _
from lino.core.gfks import gfk2lookup
from lino.core.utils import model_class_path
from lino import mixins
from lino.mixins.sequenced import Sequenced
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.office.roles import OfficeUser, OfficeStaff, OfficeOperator
from lino.mixins import Hierarchical
from lino.utils.mldbc.mixins import BabelDesignated
# from lino.modlib.uploads.mixins import UploadBase, safe_filename, FileUsable, GalleryViewable
from lino.modlib.uploads.mixins import UploadBase, safe_filename, GalleryViewable
from lino.core import constants


# class ShowGallery(dd.ShowTable):
#     # select_rows = False
#     pass


def filename_leaf(name):
    i = name.rfind('/')
    if i != -1:
        return name[i + 1:]
    return name


class Album(BabelDesignated, Hierarchical):

    class Meta(object):
        abstract = dd.is_abstract_model(__name__, 'Album')
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")


dd.inject_field('uploads.Upload', 'album',
    dd.ForeignKey("albums.Album", blank=True, null=True))


class AlbumDetail(dd.DetailLayout):
    main = """
    treeview_panel general
    """

    general = """
    designation id parent
    FilesByAlbum #AlbumsByAlbum
    """

class Albums(dd.Table):
    model = 'albums.Album'
    required_roles = dd.login_required(OfficeStaff)

    column_names = "designation parent *"
    detail_layout = "albums.AlbumDetail"
    insert_layout = "designation parent"



from lino.modlib.uploads.models import Uploads

class FilesByAlbum(Uploads):
    master_key = "album"
    display_mode = ((None, constants.DISPLAY_MODE_GALLERY), )
    column_names = "file description thumbnail *"


class AlbumsByAlbum(Albums):
    label = "Albums"
    master_key = "parent"


# class FileUsages(dd.Table):
#     model = 'albums.FileUsage'
#     required_roles = dd.login_required((OfficeUser, OfficeOperator))
#
#     detail_layout = """
#     file id
#     file__file_size
#     file__thumbnail
#     owner seqno primary_image
#     """
#
#     insert_layout = """
#     file
#     upload_new_file
#     seqno primary_image delete_old_primary_image_field
#     """
#
#     @classmethod
#     def get_choices_text(cls, obj, request, field):
#         if str(field) == 'albums.FileUsage.file':
#             return str(obj) + "&nbsp;<span style=\"float: right;\">" + obj.thumbnail + "</span>"
#         return str(obj)
#
#
#
# class UsagesByController(FileUsages):
#     label = _("Media files")
#     master_key = 'owner'
#     column_names = "seqno file file__thumbnail *"
#     display_mode = ((None, constants.DISPLAY_MODE_GALLERY), )
#     # summary_sep = lambda : ", "


# @dd.receiver(dd.post_startup)
# def setup_memo_commands(sender=None, **kwargs):
#     # See :doc:`/specs/memo`
#
#     if not sender.is_installed('memo'):
#         return
#
#     mp = sender.plugins.memo.parser
#
#     # def manage_file_usage(ar, usages):
#     #     if ar is None or len(ar.selected_rows) != 1: return
#     #
#     #     usages = set(usages)
#     #     owner = ar.selected_rows[0]
#     #     FileUsage = rt.models.albums.FileUsage
#     #     lookup = gfk2lookup(FileUsage.owner, owner)
#     #     qs = set(FileUsage.objects.filter(**lookup))
#     #     for obj in qs:
#     #         if obj.file not in usages:
#     #             qs.remove(obj)
#     #             obj.delete()
#     #     qs = {obj.file for obj in qs}
#     #     for file in usages.difference(qs):
#     #         fu = FileUsage(file=file, **lookup)
#     #         fu.full_clean()
#     #         fu.save()
#
#     def render_img_thumbnail(ar, s, cmdname, usages):
#         args = s.split(None, 1)
#         if len(args) == 1:
#             pk = s
#             caption = None
#         else:
#             pk = args[0]
#             caption = args[1]
#
#         file = rt.models.albums.File.objects.get(pk=pk)
#
#         if usages.get(cmdname, None) is None:
#             usages[cmdname] = [file]
#         else:
#             usages[cmdname].append(file)
#
#         thumbnail = file.thumbnail_large
#
#         if file.description is not None and caption is None:
#             caption = file.description
#
#         elem = (f'<figure class="lino-memo-image">{thumbnail}<figcaption' +
#             ' style="text-align: center;">{caption}</figcaption></figure>')
#
#         return elem
#
#     mp.register_django_model('image', rt.models.albums.File)
#         # cmd=render_img_thumbnail,
#         # manage_usage=manage_file_usage,
#         # title=lambda obj: obj.description)
