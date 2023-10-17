# -*- coding: UTF-8 -*-
# Copyright 2009-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
from io import StringIO
from lxml import etree
from html import escape

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext
from django.utils import timezone

from lino.api import dd, rt
from lino import mixins
from lino.core import constants
from lino.core.gfks import gfk2lookup, ContentType
from lino.modlib.uploads.mixins import UploadBase
from lino.core.utils import models_by_base
from lino.modlib.gfks.mixins import Controllable
from lino_xl.lib.topics.models import AddInterestField
from lino.modlib.users.mixins import My, UserAuthored
from lino.modlib.comments.mixins import Commentable
from lino.modlib.publisher.mixins import Publishable
from lino.modlib.publisher.choicelists import PublisherViews
# from lino.modlib.printing.mixins import PrintableType, TypedPrintable
from lino.mixins.periods import CombinedDateTime
from lino.core.requests import BaseRequest
from lino.modlib.memo.mixins import Previewable
from lino.utils import join_elems
from etgen.html import E, tostring

from .roles import BlogsReader
from .choicelists import EntryStates

from lino.modlib.office.roles import OfficeUser

html_parser = etree.HTMLParser()


class EntryType(mixins.BabelNamed):

    templates_group = 'blogs/Entry'

    class Meta():
        app_label = 'blogs'
        abstract = dd.is_abstract_model(__name__, 'EntryType')
        verbose_name = _("Blog Entry Type")
        verbose_name_plural = _("Blog Entry Types")

    #~ name = models.CharField(max_length=200)
    important = models.BooleanField(
        verbose_name=_("important"),
        default=False)
    remark = models.TextField(verbose_name=_("Remark"), blank=True)

    def __str__(self):
        return self.name


class EntryTypes(dd.Table):
    model = 'blogs.EntryType'
    # column_names = 'name build_method template *'
    order_by = ["name"]

    detail_layout = """
    id name
    # build_method template
    remark:60x5
    blogs.EntriesByType
    """


class Entry(UserAuthored, Controllable, CombinedDateTime,
            Previewable, Publishable, Commentable):

    class Meta:
        app_label = 'blogs'
        abstract = dd.is_abstract_model(__name__, 'Entry')
        verbose_name = _("Blog Entry")
        verbose_name_plural = _("Blog Entries")

    title = models.CharField(_("Heading"), max_length=200, blank=True)
    pub_date = models.DateField(
        _("Publication date"), blank=True, null=True)
    pub_time = dd.TimeField(
        _("Publication time"), blank=True, null=True)
    entry_type = dd.ForeignKey('blogs.EntryType', blank=True, null=True)
    language = dd.LanguageField()
    state = EntryStates.field(default='draft')

    def __str__(self):
        if self.title:
            return self.title
        if self.pub_date:
            return _("{} by {}").format(self.pub_date, self.user)
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

    def on_create(self, ar):
        # Sets the :attr:`pub_date` and :attr:`pub_time` to now.
        if not settings.SITE.loading_from_dump:
            self.set_datetime('pub', timezone.now())
            self.language = ar.get_user().language
        super().on_create(ar)

    def on_duplicate(self, ar, master):
        self.state = EntryStates.draft
        super().on_duplicate(ar, master)

    add_interest = AddInterestField()

    # def get_detail_action(self, ar):
    #     user = ar.get_user()
    #     if user.user_type.has_required_roles([BlogsReader]) and \
    #         user == self.user:
    #         return super().get_detail_action(ar)
    #     return rt.models.blogs.PublicEntries.detail_action

    @dd.htmlbox(_("Preview"))
    def preview(self, ar):
        if ar is None:
            return
        return ''.join(ar.row_as_page(self))

    def is_public(self):
        return self.state.is_public

    # def get_item_preview(self, ar):
    #     if ar is None:
    #         return
    #     return ar.row_as_paragraph(self)

    # @dd.htmlbox()
    # def item_preview(self, ar):
    #     return self.get_item_preview(ar)

    def as_story_item(self, ar):
        if ar is None:
            return
        return ''.join(ar.row_as_page(self))
        # return ar.row_as_paragraph(self)

    # def get_primary_image(self):
    #     Mention = rt.models.memo.Mention
    #     # stypes = [ContentType.objects.get_for_model(m)
    #     #     for m in models_by_base(UploadBase)]
    #     # qs = Mention.objects.filter(**gfk2lookup(
    #     #     Mention.owner, self, source_type__in=stypes))
    #     file_type = ContentType.objects.get_for_model(rt.models.uploads.Upload)
    #     qs = Mention.objects.filter(**gfk2lookup(
    #         Mention.owner, self, source_type=file_type))
    #         # Mention.owner, self, source_type__in=stypes))
    #     for obj in qs:
    #         if obj.source.file is not None:
    #             return obj.source

    def as_page(self, ar, **kwargs):
        title = self.title or self
        # img = self.get_primary_image()
        pub_info = _("Published {date} by {author}").format(
            date=self.pub_date.isoformat(),
            author=tostring(ar.obj2html(self.user)))
        if False:  # ar.get_user() == self.user:
            btn = tostring(ar.row_action_button(self,
                    rt.models.blogs.MyEntries.detail_action, label='edit',
                    icon_name=None, CLASS='pi pi-pencil'))
            title += '<span style="float: right;">{}</span>'.format(btn)

        # yield """<div style="display:flex; max-width:80ch; margin:auto;">"""
        yield """<div style="max-width:80ch; margin:auto;">"""
        yield "<h1>{}</h1>".format(title)
        # if img is not None:
        #     yield """
        #     <p><figure>
        #     {img.thumbnail_large}
        #     <figcaption style="text-align: center;">{img.description}</figcaption>
        #     </figure></p>
        #     """.format(img=img, obj=self)
        yield """<p><em>{}</em></p>""".format(pub_info)
        yield """<hr/>"""
        yield self.body_full_preview
        yield "</div>"

    def as_paragraph(self, ar):
        title = self.title or self
        pub_info = _("Published {date} by {author}").format(
            date=self.pub_date.isoformat(), author=self.user)
        # url = escape(ar.obj2url(self))
        # url = self.publisher_url(ar)
        url = escape(ar.obj2url(self))
        s = """<a href="{}"><strong>{}</strong> — """.format(url, title)
        s += """<span style="font-size:70%;"><em>{}</em></span></a>""".format(pub_info)
        # s += "<p>{}</p>".format(self.body_short_preview)
        s += """<div style="display:flex;">"""
        # img = self.get_primary_image()
        # if img is not None:
        #     s += f"""<div style="margin-right:20px;"><a href="{url}">{img.thumbnail}</a></div>"""
        # else:
        #     s += """<div>no image</div>"""
        s += """<div><p style="text-align:justify;">"""
        s += self.body_short_preview
        s += """</p></div>"""
        s += """</div>"""
        return s

    @classmethod
    def get_dashboard_items(cls, user):
        qs = cls.objects.filter(pub_date__isnull=False).order_by("-pub_date")
        return qs[:5]

    @classmethod
    def get_dashboard_objects(cls, ar):
        # qs = cls.objects.filter(pub_date__isnull=False).order_by('-pub_date')
        # return qs[:5]
        return cls.get_dashboard_items(ar.get_user())


    # @classmethod
    # def latest_entries(cls, ar, max_num=10, **context):
    #     context = ar.get_printable_context(**context)
    #     qs = cls.objects.filter(pub_date__isnull=False)
    #     qs = qs.order_by("-pub_date")
    #     s = ''
    #     render = dd.plugins.jinja.render_jinja
    #     for num, e in enumerate(qs):
    #         if num >= max_num:
    #             break
    #         context.update(obj=e)
    #         s += render(ar, 'blogs/entry.html', context)
    #     return s


# class Tagging(dd.Model):
#     """A **tag** is the fact that a given entry mentions a given topic.

#     """
#     class Meta:
#         app_label = 'blogs'
#         verbose_name = _("Tagging")
#         verbose_name_plural = _('Taggings')

#     allow_cascaded_delete = ['entry', 'topic']

#     topic = dd.ForeignKey(
#         'topics.Topic',
#         related_name='tags_by_topic')

#     entry = dd.ForeignKey(
#         'blogs.Entry',
#         related_name='tags_by_entry')


class EntryDetail(dd.DetailLayout):
    main = "preview general more"

    general = dd.Panel("""
    title entry_type:12 id
    # summary
    pub_date pub_time user:10 language:10 owner
    body:60  #TaggingsByEntry:20
    """, label=_("General"), required_roles=dd.login_required(OfficeUser))

    more = dd.Panel("""
    topics.InterestsByController:20 add_interest
    comments.CommentsByRFC:20
    """, label=_("More"), required_roles=dd.login_required(OfficeUser))



class ItemLayout(dd.DetailLayout):
    main = "layout"

    layout = "meta:30 body_short_preview:70"

    meta = """
    user
    pub_date
    """


class Entries(dd.Table):
    required_roles = set([BlogsReader])

    model = 'blogs.Entry'
    column_names = "id pub_date user entry_type title *"
    order_by = ["-id"]

    hide_top_toolbar = False

    display_mode = ((None, constants.DISPLAY_MODE_LIST), )

    insert_layout = """
    title
    entry_type
    """

    detail_layout = EntryDetail()
    list_layout = ItemLayout()

    @classmethod
    def collect_extra_actions(cls):
        yield dd.WrappedAction(
            rt.models.blogs.PublicEntries.detail_action,
            label=_("Pretty view"),
            icon_name=None)


class PublicEntries(Entries):
    required_roles = set()  # also for anonymous
    # hide_top_toolbar = True
    # detail_layout = """
    # preview
    # comments.CommentsByRFC
    # """

    display_mode = ((None, constants.DISPLAY_MODE_STORY), )

    @classmethod
    def collect_extra_actions(cls):
        return []

PublisherViews.add_item_lazy("b", PublicEntries)

class MyEntries(My, Entries):
    required_roles = dd.login_required(BlogsReader, dd.SiteStaff)
    #~ master_key = 'user'
    column_names = "id pub_date entry_type title body *"
    # order_by = ["-modified"]

class AllEntries(Entries):
    required_roles = dd.login_required(dd.SiteStaff)

#~ class NotesByProject(Notes):
    #~ master_key = 'project'
    #~ column_names = "date subject user *"
    #~ order_by = "date"

#~ class NotesByController(Notes):
    #~ master_key = 'owner'
    #~ column_names = "date subject user *"
    #~ order_by = "date"


class EntriesByType(Entries):
    master_key = 'entry_type'
    column_names = "pub_date title user *"
    order_by = ["pub_date-"]
    #~ label = _("Notes by person")


class EntriesByController(Entries):
    master_key = 'owner'
    column_names = "pub_date title user *"
    order_by = ["-pub_date"]
    display_mode = ((None, constants.DISPLAY_MODE_SUMMARY), )

    @classmethod
    def get_table_summary(self, mi, ar):
        if ar is None:
            return ''
        sar = self.request_from(ar, master_instance=mi)

        def fmt(obj):
            return str(obj)

        elems = []
        for obj in sar:
            # if len(elems) > 0:
            #     elems.append(', ')

            lbl = fmt(obj)
            # if obj.state.button_text:
            #     lbl = "{0}{1}".format(lbl, obj.state.button_text)
            elems.append(ar.obj2html(obj, lbl))
        elems = join_elems(elems, sep=', ')
        toolbar = []
        ar2 = self.insert_action.request_from(sar)
        if ar2.get_permission():
            btn = ar2.ar2button()
            toolbar.append(btn)

        if len(toolbar):
            toolbar = join_elems(toolbar, sep=' ')
            elems.append(E.p(*toolbar))

        return ar.html_text(E.div(*elems))



class LatestEntries(PublicEntries):
    """Show the most recent blog entries."""
    label = _("Latest blog entries")
    column_names = "pub_date title user *"
    order_by = ["-pub_date"]
    filter = models.Q(pub_date__isnull=False)
    display_mode = ((None, constants.DISPLAY_MODE_LIST), )
    editable = False

    @classmethod
    def get_table_summary(cls, obj, ar, max_num=10, **context):

        context = ar.get_printable_context(**context)
        qs = rt.models.blogs.Entry.objects.filter(pub_date__isnull=False)
        qs = qs.order_by("-pub_date")
        render = dd.plugins.jinja.render_jinja
        elems = []
        for num, e in enumerate(qs):
            if num >= max_num:
                break
            context.update(obj=e)
            # s = render(ar, 'blogs/entry.html', context)
            elems.append(E.h2(e.title or str(e), " ", e.obj2href(
                ar, "⏏", **{'style': "text-decoration:none"})))
            # s = ar.parse_memo(e.body_short_preview)
            s = e.body_short_preview
            tree = etree.parse(StringIO(s), html_parser)
            # elems.extend(tree.iter())
            # elems.append(tree.iter().next())
            elems.append(tree.getroot())
            elems.append(E.p(
                _("{} by {}").format(dd.fdf(e.pub_date), e.user)))
            # elems.append(E.p(
            #     _("{} by {}").format(dd.fdf(e.pub_date), e.user),
            #     " ", e.obj2href(ar, "(edit)")))

        return E.div(*elems)

# PublisherViews.add_item_lazy("latest", LatestEntries)

from lino_xl.lib.pages.choicelists import DataViewNodeType
DataViewNodeType(LatestEntries).register()


# class Taggings(dd.Table):
#     model = 'blogs.Tagging'

# class AllTaggings(Taggings):
#     required_roles = dd.login_required(dd.SiteStaff)

# class TaggingsByEntry(Taggings):
#     master_key = 'entry'
#     column_names = 'topic *'

# class TaggingsByTopic(Taggings):
#     master_key = 'topic'
#     column_names = 'entry *'
