# -*- coding: UTF-8 -*-
# Copyright 2012-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lorem import get_paragraph
from django.utils import translation
from django.conf import settings
from lino.api import rt, dd, _
from lino.utils import Cycler

welcome = _("""Welcome to our great website. We are proud to present
the best content about foo, bar and baz.
""")

# BODIES = Cycler([lorem, short_lorem])
# blog_body = "[eval sar.show(settings.SITE.models.blogs.LatestEntries)]"
# blog_body = "[show blogs.LatestEntries]"
PARA = "<p>" + get_paragraph(count=2, sep="</p><p>") + "</p>"
blog_body = _("This page shows the most recent blog entries.")
photos_children = []

def add(*args):
    photos_children.append(args)

add(_("Default formatting"), "<p align=\"center\">[upload 6]</p><p><tt>\\[upload 6]</tt> inserts the image without any text wrapping. "+get_paragraph(), None, [])
add(_("Thumbnail"), "[upload 6 thumb|] <tt>\\[upload 6 thumb|]</tt> makes the image float right with a height of 10em. "+get_paragraph()+PARA, None, [])
add(_("Thumbnail left"), "[upload 6 thumb|left|]  <tt>\\[upload 6 thumb|left|]</tt> makes the image float left instead of right. "+get_paragraph()+PARA, None, [])
add(_("Tiny thumbnail"), "[upload 6 tiny|] "+get_paragraph()+PARA, None, [])
add(_("Tiny thumbnail left"), "[upload 6 tiny|left|] "+get_paragraph()+PARA, None, [])
# add(_("trio"), PARA + "<p align=\"center\">[upload 11 trio|] [upload 12 trio|] [upload 8 trio|]</p>"+PARA, None, [])
# add(_("duo"), PARA + "<p align=\"center\">[upload 11 duo|] [upload 6 duo|]</p>"+PARA, None, [])
# add(_("solo"), PARA + "<p align=\"center\">[upload 11 solo|]</p>"+PARA, None, [])
add(_("Wide"), PARA + "[upload 11 wide|]"+PARA, None, [])
# add("[photorow]", PARA + "[photorow 5 6 7 8]"+PARA, None, [])
add(_("Gallery"), "<p>The <tt>\[gallery ]</tt> command accepts any number of primary keys and inserts a centered paragraph with these pictures.</p>" + "[gallery 5 6 7 8 9 10 11 13 14]"+PARA, None, [])


home_children = [
    (_("Services"), None, None, [
        (_("Washing"), None, None, []),
        (_("Drying"), None, None, [
            (_("Air drying"), None, None, []),
            (_("Machine drying"), None, None, [])]),
        (_("Ironing"), None, None, []),
    ]),
    (_("Prices"), None, None, []),
    (_("Photos"), None, None, photos_children),
    (_("About us"), None, None, [
        (_("Team"), None, None, []),
        (_("History"), None, None, []),
        (_("Contact"), None, None, []),
        (_("Terms & conditions"), None, None, []),
    ])
]
if dd.is_installed("blogs"):
    home_children.append((_("Blog"), blog_body, "blogs.LatestEntries", []))
if dd.is_installed("comments"):
    home_children.append((_("Recent comments"), "", "comments.RecentComments", []))
site_pages = [
    (_("Home"), welcome, None, home_children)
]

# from pprint import pprint
# pprint(pages)

def objects():
    Node = rt.models.pages.Node
    # for lc in settings.SITE.LANGUAGE_CHOICES:
    #     language = lc[0]
    #     kwargs = dict(language=language, ref='index')
    #     with translation.override(language):
    # counter = {None: 0}

    def make_pages(pages, parent=None):
        for title, body, node_type, children in pages:
            kwargs = dict()
            if parent is None:
                kwargs.update(ref='index')
            kwargs = dd.str2kw("title", title, **kwargs)
            if node_type:
                kwargs.update(node_type=node_type)
            if body is None:
                kwargs.update(body=get_paragraph())
            else:
                kwargs = dd.str2kw("body", body, **kwargs)
            # for i in range(counter[None]):
            #     body += paragraph()
            # if counter[None] > 0:
            #     kwargs.pop('ref', None)
            # p = Node(title=str(title), body=str(body), parent=parent, **kwargs)
            p = Node(parent=parent, **kwargs)
            yield p
            # ref = None
            # counter[None] += 1
            # print("20230324", title, kwargs)
            yield make_pages(children, p)
    yield make_pages(site_pages)
