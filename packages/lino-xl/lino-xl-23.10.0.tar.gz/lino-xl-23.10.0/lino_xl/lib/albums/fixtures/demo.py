# -*- coding: UTF-8 -*-
# Copyright 2009-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from pathlib import Path
from lino.api import rt, dd, _
from lino.utils import Cycler
from lino.modlib.uploads.mixins import make_uploaded_file

srcpath = Path(__file__).parent

def walk(p):
    # print("20230331", p)
    for c in sorted(p.iterdir()):
        if c.is_dir():
            for cc in walk(c):
                yield cc
        else:
            yield c

def objects():
    Album = rt.models.albums.Album
    File = rt.models.uploads.Upload
    # FileUsage = rt.models.albums.FileUsage

    demo_date = dd.demo_date()

    top = Album(**dd.str2kw("designation", _("All")))
    yield top
    yield Album(parent=top, **dd.str2kw("designation", _("Furniture")))
    yield Album(parent=top, **dd.str2kw("designation", _("Things")))
    yield Album(parent=top, **dd.str2kw("designation", _("Services")))

    books = Album(parent=top, **dd.str2kw("designation", _("Books")))
    yield books

    yield Album(parent=books, **dd.str2kw("designation", _("Biographies")))
    yield Album(parent=books, **dd.str2kw("designation", _("Business")))
    yield Album(parent=books, **dd.str2kw("designation", _("Culture")))
    yield Album(parent=books, **dd.str2kw("designation", _("Children")))
    yield Album(parent=books, **dd.str2kw("designation", _("Medicine")))

    thrill = Album(parent=books, **dd.str2kw("designation", _("Thriller")))
    yield thrill

    for cover in """\
MurderontheOrientExpress.jpg Murder_on_the_orient_express_cover
StormIsland.jpg Storm_island_cover
AndThenThereWereNone.jpg And_then_there_were_none
FirstThereWereTen.jpg First_there_were_ten
""".splitlines():
        name, description = cover.split()
        file = make_uploaded_file(name, srcpath / "images" / name, demo_date)
        yield File(album=thrill, file=file, description=description.replace('_', ' '))

    # if dd.is_installed('products'):
    #     FILES = Cycler(File.objects.all())
    #     OWNERS = Cycler(rt.models.products.Product.objects.all())
    #     for i in range(10):
    #         yield FileUsage(file=FILES.pop(), owner=OWNERS.pop())

    Volume = rt.models.uploads.Volume
    root_dir = srcpath.parent / 'static/albums/photos'
    vol = Volume(ref="demo", description="Photo album",
        root_dir=root_dir, base_url="albums/photos")
    yield vol
    photos = Album(parent=top, **dd.str2kw("designation", _("Photos")))
    yield photos

    chop = len(str(root_dir)) + 1
    for fn in walk(root_dir):
        fns = str(fn)[chop:]
        # print("20230325 {}".format(fn))
        yield File(album=photos, volume=vol, library_file=fns,
            description=fns.replace('_', ' ').replace('/', ' '),
            copyright=fn.parent.name + " Luc Saffre")
