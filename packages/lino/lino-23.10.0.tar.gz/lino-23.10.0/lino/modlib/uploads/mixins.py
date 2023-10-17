# -*- coding: UTF-8 -*-
# Copyright 2008-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
import shutil
from pathlib import Path

from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError, FieldError
from django.template.defaultfilters import filesizeformat

from etgen.html import E
from rstgen.sphinxconf.sigal_image import parse_image_spec
from lino.api import dd, rt, _
from lino.modlib.memo.mixins import MemoReferrable
# from lino.mixins.sequenced import Sequenced
# from lino.modlib.gfks.mixins import Controllable
from .choicelists import UploadAreas


def safe_filename(name):
    name = name.encode('ascii', 'replace').decode('ascii')
    name = name.replace('?', '_')
    name = name.replace('/', '_')
    name = name.replace(' ', '_')
    return name


def needs_update(src, dest):
    if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
        return False
    return True


def make_uploaded_file(filename, src=None, upload_date=None):
    """
    Create a dummy file that looks as if a file had really been uploaded.

    """
    if src is None:
        src = Path(__file__).parent / "dummy_upload.pdf"
    if upload_date is None:
        upload_date = dd.demo_date()
    assert src.exists()
    filename = default_storage.generate_filename(safe_filename(filename))
    upload_to = Path(upload_date.strftime(settings.SITE.upload_to_tpl))
    upload_filename = default_storage.generate_filename(str(upload_to / filename))
    dest = Path(settings.MEDIA_ROOT) / upload_filename
    if needs_update(src, dest):
        print("cp {} {}".format(src, dest))
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    return upload_filename


def demo_upload(filename, src=None, upload_date=None, **kw):
    """
    Return an upload entry that looks as if a file had really been uploaded.

    """
    kw['file'] = make_uploaded_file(filename, src, upload_date)
    return rt.models.uploads.Upload(**kw)


# class FileUsable(Sequenced, Controllable):
#
#     class Meta:
#         abstract = True
#
#     file = None
#
#     @classmethod
#     def on_analyze(cls, site):
#         if cls.file is None:
#             raise FieldError("Set 'file' field to ForeignKey pointing to a file model.")
#         return super().on_analyze(site)


class UploadController(dd.Model):
    class Meta(object):
        abstract = True

    def get_upload_area(self):
        return UploadAreas.general

    def get_uploads_volume(self):
        return None

    if dd.is_installed("uploads"):
        show_uploads = dd.ShowSlaveTable(
            'uploads.UploadsByController',
            react_icon_name="pi-upload",
            button_text="❏")  # 274f
        # button_text="⍐")  # 2350
        # button_text="🖿")  # u"\u1F5BF"

        show_uploads = dd.ShowSlaveTable(
            'uploads.UploadsByController',
            react_icon_name="pi-upload",
            button_text="❏")  # 274f


class GalleryViewable(dd.Model):
    class Meta(object):
        abstract = True

    def get_gallery_item(self, ar):
        return {}


class UploadBase(MemoReferrable, GalleryViewable):
    class Meta(object):
        abstract = True

    file = models.FileField(
        _("File"), blank=True, upload_to=settings.SITE.upload_to_tpl)
    mimetype = models.CharField(
        _("MIME type"), blank=True, max_length=255, editable=False)
    file_size = models.IntegerField(_("File size"), editable=False, null=True)

    def handle_uploaded_files(self, request, file=None):
        # ~ from django.core.files.base import ContentFile
        if not file and not 'file' in request.FILES:
            dd.logger.debug("No 'file' has been submitted.")
            return
        uf = file or request.FILES['file']  # an UploadedFile instance

        self.save_newly_uploaded_file(uf)

    def save_newly_uploaded_file(self, uf):
        # ~ cf = ContentFile(request.FILES['file'].read())
        # ~ print f
        # ~ raise NotImplementedError
        # ~ dir,name = os.path.split(f.name)
        # ~ if name != f.name:
        # ~ print "Aha: %r contains a path! (%s)" % (f.name,__file__)
        self.size = uf.size
        self.mimetype = uf.content_type

        # Certain Python versions or systems don't manage non-ascii filenames,
        # so we replace any non-ascii char by "_". In Py3, encode() returns a
        # bytes object, but we want the name to remain a str.

        # ~ dd.logger.info('20121004 handle_uploaded_files() %r',uf.name)
        name = safe_filename(uf.name)

        # Django magics:
        self.file = name  # assign a string
        ff = self.file  # get back a FileField instance !
        # ~ print 'uf=',repr(uf),'ff=',repr(ff)

        # ~ if not ispure(uf.name):
        # ~ raise Exception('uf.name is a %s!' % type(uf.name))

        ff.save(name, uf, save=False)

        # The expression `self.file`
        # now yields a FieldFile instance that has been created from `uf`.
        # see Django FileDescriptor.__get__()

        dd.logger.info("Wrote uploaded file %s", ff.path)

    def get_gallery_item(self, ar):
        return dict(image_src=self.get_file_url())

    def full_clean(self, *args, **kw):
        super().full_clean(*args, **kw)
        self.file_size = self.get_real_file_size()

    def get_real_file_size(self):
        return None

    def get_file_button(self, text=None):
        if text is None:
            text = str(self)
        if self.file.name:
            url = self.get_file_url()
            if url is not None:
                return E.a(text, href=url, target="_blank")
        return text

    def memo2html(self, ar, text, **ctx):
        # if not text:
        #     text = self.description or str(self)
        # ctx = dict()
        # text = src + "|" + text
        url = self.get_file_url()
        if url is None:
            return ""
        ctx.update(src=url)
        ctx.update(href=ar.renderer.obj2url(ar, self))
        if url.endswith(".pdf"):
            if not text:
                text = str(self)
            ctx.update(text=text)
            tpl = '(<a href="{src}" target="_blank"/>{text}</a>'
            tpl += '| <a href="{href}""/>detail</a>)'
            return tpl.format(**ctx)

        fmt = parse_image_spec(text, **ctx)
        if not fmt.context['caption']:
            fmt.context['caption'] = self.description or str(self)
        # if text:
        #     ctx.update(caption=text)

        rv = ('<a href="{href}" target="_blank"/><img src="{src}"' +
              ' style="{style}" title="{caption}"/></a>').format(**fmt.context)
        # if ar.renderer.front_end.media_name == 'react':
        #     return ('<figure class="lino-memo-image"><img src="{src}" ' +
        #         'style="{style}" title="{caption}"/><figcaption' +
        #         ' style="text-align: center;">{caption}</figcaption>' +
        #         '</figure>').format(**kwargs)

        # print("20230325", rv)
        return rv
