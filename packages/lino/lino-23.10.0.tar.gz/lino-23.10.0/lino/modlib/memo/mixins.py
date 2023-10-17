# -*- coding: UTF-8 -*-
# Copyright 2016-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from bs4 import BeautifulSoup, NavigableString
from bs4.element import Tag
from lxml import html as lxml_html
from etgen.html import E, tostring
import lxml

from django.conf import settings
from django.utils import translation
from django.utils.text import Truncator

from lino.core.gfks import gfk2lookup
from lino.core.model import Model
from lino.core.fields import fields_list, RichTextField, PreviewTextField
from lino.utils.restify import restify
from lino.utils.mldbc.fields import BabelTextField
from lino.core.exceptions import ChangedAPI
from lino.modlib.checkdata.choicelists import Checker
from lino.api import rt, dd, _


def old_truncate_comment(html_str, max_p_len=None):
    # returns a single paragraph with a maximum number of visible chars.
    # No longer used. Replaced by new truncate_comment() below
    if max_p_len is None:
        max_p_len = settings.SITE.plugins.memo.short_preview_length
    html_str = html_str.strip()  # remove leading or trailing newlines

    if not html_str.startswith('<'):
        if len(html_str) > max_p_len:
            txt = html_str[:max_p_len] + "..."
        else:
            txt = html_str
        return txt
    soup = BeautifulSoup(html_str, "html.parser")
    ps = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "pre"])
    if len(ps) > 0:
        anchor_end = '</a>'
        txt = ""
        for p in ps:
            text = ""
            for c in p.contents:
                if isinstance(c, Tag):
                    if c.name == 'a':
                        text += str(c)
                        max_p_len = max_p_len + len(text) - len(c.text)
                    else:
                        # text += str(c)
                        text += c.text
                else:
                    text += str(c)

            if len(txt) + len(text) > max_p_len:
                txt += text
                if anchor_end in txt:
                     ae_index = txt.index(anchor_end) + len(anchor_end)
                     if ae_index >= max_p_len:
                         txt = txt[:ae_index]
                         txt += "..."
                         break
                txt = txt[:max_p_len]
                txt += "..."
                break
            else:
                txt += text + "\n\n"
        return txt
    return html_str


def django_truncate_comment(html_str):
    # works, but we don't use it because (...)
    return Truncator(html_str).chars(settings.SITE.plugins.memo.short_preview_length, html=True)


PARAGRAPH_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "pre", "li", "div"}
WHITESPACE_TAGS = PARAGRAPH_TAGS | {"[document]", "span", "ul"}

class TextCollector:

    def __init__(self, max_length=None):
        self.text = ''
        self.sep = '' # becomes "\n\n" after a PARAGRAPH_TAGS
        self.remaining = max_length or settings.SITE.plugins.memo.short_preview_length

    def add_chunk(self, ch):
        # print("20230712 add_chunk", ch.name, ch)
        if ch.name in WHITESPACE_TAGS:
            for c in ch.children:
                if not self.add_chunk(c):
                    return False
            if ch.name in PARAGRAPH_TAGS:
                self.sep = "\n\n"
            else:
                self.sep = ' '
            return True

        we_want_more = True
        if ch.string is not None:
            if len(ch.string) > self.remaining:
                # print("20230712", len(ch.string), '>', self.remaining)
                ch.string = ch.string[:self.remaining] + "..."
                we_want_more = False
                # print("20230927", ch.string, ch)
                # self.text += str(ch.string) + "..."
                # return False
            self.remaining -= len(ch.string)

        if isinstance(ch, NavigableString):
            self.text += self.sep + ch.string
        else:
            self.text += self.sep + str(ch)

        self.remaining -= len(self.sep)
        self.sep = ''
        return we_want_more


def truncate_comment(html_str, max_length=None):
    # new implementation since 20230713
    if max_length is None:
        max_length = settings.SITE.plugins.memo.short_preview_length
    html_str = html_str.strip()  # remove leading or trailing newlines

    if not html_str.startswith('<'):
        if len(html_str) > max_length:
            txt = html_str[:max_length] + "..."
        else:
            txt = html_str
        return txt
    # if "choose one or the other" in html_str:
    #     print(html_str)
    #     raise Exception("20230928 {} {}".format(len(html_str), max_length))

    soup = BeautifulSoup(html_str, "html.parser")
    tc = TextCollector(max_length)
    tc.add_chunk(soup)
    return tc.text



def rich_text_to_elems(ar, description):
    if description.startswith("<"):
        # desc = E.raw('<div>%s</div>' % self.description)
        desc = lxml_html.fragments_fromstring(ar.parse_memo(description))
        return desc
    # desc = E.raw('<div>%s</div>' % self.description)
    html = restify(ar.parse_memo(description))
    # logger.info(u"20180320 restify %s --> %s", description, html)
    # html = html.strip()
    try:
        desc = lxml_html.fragments_fromstring(html)
    except Exception as e:
        raise Exception(
            "Could not parse {!r} : {}".format(html, e))
    # logger.info(
    #     "20160704c parsed --> %s", tostring(desc))
    return desc
    # if desc.tag == 'body':
    #     # happens if it contains more than one paragraph
    #     return list(desc)  # .children
    # return [desc]

def body_subject_to_elems(ar, title, description):
    if description:
        elems = [E.p(E.b(title), E.br())]
        elems += rich_text_to_elems(ar, description)

    else:
        elems = [E.b(title)]
        # return E.span(self.title)
    return elems


class MemoReferrable(dd.Model):
    class Meta:
        abstract = True

    memo_command = None

    @classmethod
    def on_analyze(cls, site):
        super().on_analyze(site)

        if cls.memo_command is None or not site.is_installed('memo'):
            return

        site.plugins.memo.parser.register_django_model(cls.memo_command, cls)

    # def get_memo_title(self):
    #    """A text to be used as title of the ``<a href>``."""
    #    return None
       # return str(self)

    def memo2html(self, ar, txt, **kwargs):
        if txt:
            kwargs.update(title=txt)
        e = self.obj2href(ar, **kwargs)
        return tostring(e)
        # return ar.obj2str(self, **kwargs)

        # return "<p>Oops, undefined memo2html()</p>"

    # def obj2memo(self, title=str):
    def obj2memo(self, text=None):
        """Render the given database object as memo markup.
        """
        if self.memo_command is None:
            return "**{}**".format(self)
        # title = self.get_memo_title()
        if text is None:
            # text = str(self)
            return "[{} {}]".format(self.memo_command, self.id)
        # return "[{} {}] ({})".format(self.memo_command, self.id, title)
        return "[{} {} {}]".format(self.memo_command, self.id, text)

# class MentionGenerator(dd.Model):
#
#     class Meta:
#         abstract = True
#
#     def get_memo_text(self):
#         return None
#
#     if dd.is_installed("memo"):
#         def after_ui_save(self, ar, cw):
#             super().after_ui_save(ar, cw)
#             memo_parser = settings.SITE.plugins.memo.parser
#             ref_objects = memo_parser.get_referred_objects(self.get_memo_text())
#             Mention = rt.models.memo.Mention
#             for ref_object in ref_objects:
#                 created_mention = Mention(owner=self,
#                         owner_id=ref_object.pk,
#                         owner_type=ContentType.objects.get_for_model(ref_object.__class__))
#                 created_mention.touch()
#                 created_mention.save()


# class BasePreviewable(MentionGenerator):
class BasePreviewable(dd.Model):
    class Meta:
        abstract = True

    previewable_field = None

    def save(self, *args, **kwargs):
        """Updates the preview fields and the list of mentioned objects.

        """
        pf = self.previewable_field
        mentions = set()
        txt = self.get_previewable_text(settings.SITE.DEFAULT_LANGUAGE)
        short, full = self.parse_previews(txt, mentions)
        # if "choose one or the other" in short:
        #     raise Exception("20230928 {} {}".format(len(short), short))
        setattr(self, pf + '_short_preview', short)
        setattr(self, pf + '_full_preview', full)
        if isinstance(self, BabelPreviewable):
            for lng in settings.SITE.BABEL_LANGS:
                src = self.get_previewable_text(lng)
                # src = getattr(self, pf + lng.suffix)
                with translation.override(lng.django_code):
                    short, full = self.parse_previews(src, mentions)
                setattr(self, pf + '_short_preview' + lng.suffix, short)
                setattr(self, pf + '_full_preview' + lng.suffix, full)
        super().save(*args, **kwargs)
        self.synchronize_mentions(mentions)

    def get_previewable_text(self, lng):
        return getattr(self, self.previewable_field+lng.suffix)

    @classmethod
    def parse_previews(self, source, mentions=None, **kwargs):
        full = settings.SITE.plugins.memo.parser.parse(
            source, mentions=mentions, **kwargs)
        short = truncate_comment(full)
        return (short, full)

    def get_saved_mentions(self):
        Mention = rt.models.memo.Mention
        flt = gfk2lookup(Mention.owner, self)
        return Mention.objects.filter(**flt).order_by('source_type', 'source_id')

    def synchronize_mentions(self, mentions):
        Mention = rt.models.memo.Mention
        for obj in self.get_saved_mentions():
            if obj.source in mentions:
                mentions.remove(obj.source)
            else:
                obj.delete()
        for source in mentions:
            obj = Mention(owner=self, source=source)
            # source_id=source.pk,
            # source_type=ContentType.objects.get_for_model(source.__class__))
            obj.full_clean()
            obj.save()

    def get_overview_elems(self, ar):
        yield E.h1(str(self))

        if self.body_short_preview:
            try:
                for e in lxml.html.fragments_fromstring(self.body_short_preview):
                    yield e
            except Exception as e:
                yield "{} [{}]".format(self.body_short_preview, e)


class Previewable(BasePreviewable):

    class Meta:
        abstract = True

    previewable_field = 'body'

    body = PreviewTextField(_("Body"), blank=True, format='html', bleached=True)
    body_short_preview = RichTextField(_("Preview"), blank=True, editable=False)
    body_full_preview = RichTextField(_("Preview (full)"), blank=True, editable=False)

    def as_paragraph(self, ar):
        s = "<b>{}</b> : ".format(ar.add_detail_link(self, str(self)))
        s += self.body_short_preview or _("(no preview)")
        return s

class BabelPreviewable(BasePreviewable):

    class Meta:
        abstract = True

    previewable_field = 'body'

    body = BabelTextField(_("Body"), blank=True, format='html', bleached=True)
    body_short_preview = BabelTextField(_("Preview"), blank=True, editable=False)
    body_full_preview = BabelTextField(_("Preview (full)"), blank=True, editable=False)

    # def save(self, *args, **kwargs):
    #     pf = self.previewable_field
    #     mentions = set()
    #     for lng in settings.SITE.BABEL_LANGS:
    #         src = getattr(self, self.previewable_field+lng.suffix)
    #         with translation.override(lng.django_code):
    #             short, full = self.parse_previews(src, mentions)
    #         setattr(self, pf+'_short_preview'+lng.suffix, short)
    #         setattr(self, pf+'_full_preview'+lng.suffix, full)
    #     super().save(*args, **kwargs)
    #     self.synchronize_mentions(mentions)


class PreviewableChecker(Checker):
    verbose_name = _("Check for previewables needing update")
    model = BasePreviewable

    def _get_checkdata_problems(self, lng, obj, fix=False):
        src = obj.get_previewable_text(lng)
        pf = obj.previewable_field
        # src = getattr(obj, pf+suffix)
        expected_mentions = set()
        short, full = obj.parse_previews(src, expected_mentions)
        is_broken = False
        if getattr(obj, pf+'_short_preview'+lng.suffix) != short \
            or getattr(obj, pf+'_full_preview'+lng.suffix) != full:
            yield (True, _("Preview differs from source."))
            is_broken = True
        found_mentions = set([obj.source for obj in obj.get_saved_mentions()])
        if expected_mentions != found_mentions:
            yield (True, _("Mentions differ from expected mentions."))
            is_broken = True
        if is_broken and fix:
            # setattr(obj, pf+'_short_preview'+suffix, short)
            # setattr(obj, pf+'_full_preview'+suffix, full)
            obj.full_clean()
            obj.save()
        # self.synchronize_mentions(mentions)

    def get_checkdata_problems(self, obj, fix=False):
        for x in self._get_checkdata_problems(settings.SITE.DEFAULT_LANGUAGE, obj, fix):
            yield x
        if isinstance(obj, BabelPreviewable):
            for lng in settings.SITE.BABEL_LANGS:
                with translation.override(lng.django_code):
                    for x in self._get_checkdata_problems(lng, obj, fix):
                        yield x

PreviewableChecker.activate()
