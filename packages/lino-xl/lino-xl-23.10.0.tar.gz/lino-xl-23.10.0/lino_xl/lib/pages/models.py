# -*- coding: UTF-8 -*-
# Copyright 2012-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from html import escape
from django.db import models
from django.utils import translation
from django.utils.translation import pgettext_lazy
# from django.utils.translation import get_language
from django.utils.html import mark_safe

from lino.api import dd, rt, _
from etgen.html import E, tostring_pretty
from lino.core import constants
# from lino.core.renderer import add_user_language

from lino.utils.mldbc.fields import LanguageField
from lino import mixins
from lino.mixins import Hierarchical, Sequenced
from lino.modlib.publisher.mixins import Publishable
from lino.modlib.publisher.choicelists import PublisherViews
from lino.modlib.memo.mixins import BabelPreviewable
from django.conf import settings
from .utils import render_node
from .choicelists import NodeTypes


class Node(Hierarchical, Sequenced, BabelPreviewable, Publishable):

    class Meta:
        verbose_name = _("Node")
        verbose_name_plural = _("Nodes")
        # unique_together = ["ref", "language"]

    ref = models.CharField(
        _("Reference"), max_length=200, blank=True, null=True)
    title = dd.BabelCharField(_("Title"), max_length=250, blank=True)
    child_node_depth = models.IntegerField(default=2)
    node_type = NodeTypes.field(blank=True, null=True)

    def is_public(self):
        return True

    def as_page(self, ar, display_mode="detail", hlevel=1, home=None):
        if home is None:
            home = self
        if display_mode == "detail" and hlevel == 1:
            breadcrumbs = list(self.get_parental_line())
            if len(breadcrumbs) > 1:
                breadcrumbs = [
                    """<a href="{0}">{1}</a>""".format(ar.obj2url(p), dd.babelattr(p, 'title'))
                    for p in breadcrumbs[:-1]]
                yield "<p>{}</p>".format(" | ".join(breadcrumbs))
        if display_mode in ("detail", "story"):
            title = "<h{0}>{1}</h{0}>".format(hlevel, escape(dd.babelattr(self, 'title')))
        else:
            title = "<b>{}</b>  — ".format(escape(dd.babelattr(self, 'title')))
            title += dd.babelattr(self, 'body_short_preview')
            title = "<li>{}</i>".format(title)
        edit_url = ar.renderer.obj2url(ar, self)
        # url = self.publisher_url(ar)
        url = ar.obj2url(self)
        if url is None:
            yield title
        else:
            yield """<a href="{}"
            style="text-decoration:none; color: black;">{}</a>
            """.format(escape(url), title)

        if display_mode in ("detail", "story"):
            yield dd.babelattr(self, 'body_full_preview')

            if self.node_type:
                yield "\n\n"
                if hlevel == 1:
                    yield self.node_type.get_dynamic_story(ar, self)
                else:
                    yield self.node_type.get_dynamic_paragraph(ar, self)

            if hlevel > home.child_node_depth:
                if self.children.exists():
                    yield " (...)"
                return
            if hlevel == home.child_node_depth:
                display_mode = 'list'
                yield "<ul>"
            for obj in self.children.order_by('seqno'):
                for i in obj.as_page(ar, display_mode, hlevel=hlevel+1, home=home):
                    yield i
            if hlevel == home.child_node_depth:
                yield "</ul>"
        # else:
        #     yield " — "
        #     yield self.body_short_preview
        #     for obj in self.children.order_by('seqno'):
        #         for i in obj.as_page(ar, "list", hlevel+1):
        #             yield i

    # @classmethod
    # def lookup_page(cls, ref):
    #     try:
    #         return cls.objects.get(ref=ref, language=get_language())
    #     except cls.DoesNotExist:
    #         pass

    @classmethod
    def get_dashboard_objects(cls, user):
        # print("20210114 get_dashboard_objects()", get_language())
        # qs = cls.objects.filter(parent__isnull=True, language=get_language())
        qs = cls.objects.filter(parent__isnull=True)
        for node in qs.order_by("seqno"):
            yield node

    def __str__(self):
        return dd.babelattr(self, 'title') or self.ref or super().__str__()

    def get_absolute_url(self, **kwargs):
        if self.ref:
            if self.ref != 'index':
                return dd.plugins.pages.build_plain_url(self.ref, **kwargs)
        return dd.plugins.pages.build_plain_url(**kwargs)

    # def get_sidebar_caption(self):
    #     if self.title:
    #         return self.title
    #     if self.ref:
    #         return self.ref
    #     return str(self.id)
    #
    #     #~ if self.ref or self.parent:
    #         #~ return self.ref
    #     #~ return unicode(_('Home'))

    # def get_sidebar_item(self, request, other):
    #     kw = dict()
    #     add_user_language(kw, request)
    #     url = self.get_absolute_url(**kw)
    #     a = E.a(self.get_sidebar_caption(), href=url)
    #     if self == other:
    #         return E.li(a, **{'class':'active'})
    #     return E.li(a)
    #
    # def get_sidebar_html(self, request):
    #     items = []
    #     #~ loop over top-level nodes
    #     for n in self.__class__.objects.filter(parent__isnull=True).order_by('seqno'):
    #         #~ items += [li for li in n.get_sidebar_items(request,self)]
    #         items.append(n.get_sidebar_item(request, self))
    #         if self.is_parented(n):
    #             children = []
    #             for ch in n.children.order_by('seqno'):
    #                 children.append(ch.get_sidebar_item(request, self))
    #             if len(children):
    #                 items.append(E.ul(*children, **{'class':'nav nav-list'}))
    #
    #     e = E.ul(*items, **{'class':'nav nav-list'})
    #     return tostring_pretty(e)
    #
    # def get_sidebar_menu(self, request):
    #     qs = self.__class__.objects.filter(parent__isnull=True, language=get_language())
    #     #~ qs = self.children.all()
    #     yield ('/', 'index', str(_('Home')))
    #         #~ yield ('/downloads/', 'downloads', 'Downloads')
    #     #~ yield ('/about', 'about', 'About')
    #     #~ if qs is not None:
    #     for obj in qs.order_by("seqno"):
    #         if obj.ref and obj.title:
    #             yield ('/' + obj.ref, obj.ref, obj.title)
    #         #~ else:
    #             #~ yield ('/','index',obj.title)


class NodeDetail(dd.DetailLayout):
    main = """
    treeview_panel:20 right_panel:60
    """
    right_panel = """
    parent seqno child_node_depth ref node_type
    title
    body:70
    pages.NodesByParent:40
    """


class Nodes(dd.Table):
    model = 'pages.Node'
    column_names = "ref title *"
    order_by = ["ref"]
    detail_layout = 'pages.NodeDetail'
    insert_layout = """
    title
    ref node_type
    """


class PublicNodes(Nodes):
    display_mode = ((None, constants.DISPLAY_MODE_STORY),)

PublisherViews.add_item_lazy("p", PublicNodes)


class NodesByParent(Nodes):
    master_key = 'parent'
    label = _("Children")
    #~ column_names = "title user *"
    order_by = ["seqno"]
    column_names = "seqno title *"
    display_mode = ((None, constants.DISPLAY_MODE_LIST),)
