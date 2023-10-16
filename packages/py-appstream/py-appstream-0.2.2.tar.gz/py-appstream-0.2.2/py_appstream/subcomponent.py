# SPDX-FileCopyrightText: 2022 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

from __future__ import annotations

import html

import dateutil.parser

from . import utils
from .exceptions import AppStreamParseError


class Node(object):
    NOT_TO_SERIALIZE = []

    def parse_tree(self, node, lang_code_func=None):
        pass

    def serialize(self):
        obj = {}
        for a, v in vars(self).items():
            if a not in type(self).NOT_TO_SERIALIZE and v:
                obj[a] = v
        return obj


class Description(Node):
    def __init__(self):
        self.object = {}

    def _prep_lang(self, n, lang_code_func):
        lang = n.get('{http://www.w3.org/XML/1998/namespace}lang', n.get('lang', 'C'))
        if lang != 'x-test':
            lang = lang_code_func(lang) if lang_code_func else lang
            if lang not in self.object:
                self.object[lang] = ''
        return lang

    def parse_tree(self, node, lang_code_func=None):
        lang_part_counts = {}
        for n in node:
            if n.tag == 'p':
                lang = self._prep_lang(n, lang_code_func)
                if lang == 'x-test':
                    continue
                if lang not in lang_part_counts:
                    lang_part_counts[lang] = 0
                self.object[lang] += f'<p>{html.escape(n.text, quote=False)}</p>\n'
                lang_part_counts[lang] += 1
            elif n.tag in ['ol', 'ul']:
                langs = set()
                for c in n:
                    if c.tag == 'li':
                        lang = self._prep_lang(c, lang_code_func)
                        if lang == 'x-test':
                            continue
                        if lang not in lang_part_counts:
                            lang_part_counts[lang] = 0
                        langs.add(lang)
                        if not (self.object[lang].endswith('</li>\n') or self.object[lang].endswith(f'<{n.tag}>\n')):
                            self.object[lang] += f'<{n.tag}>\n'
                        self.object[lang] += f'  <li>{html.escape(c.text, quote=False)}</li>\n'
                        lang_part_counts[lang] += 1
                    else:
                        raise AppStreamParseError(f'Expected <li> in <{n.tag}>, got <{c.tag}>')
                for lang in langs:
                    self.object[lang] += f'</{n.tag}>\n'
            else:
                raise AppStreamParseError(f'Expected <p>, <ul>, <ol> in <{node.tag}>, got <{n.tag}>')
        # only accept languages with number of parts not less than number of parts in the default language
        default_lang = lang_code_func('C') if lang_code_func else 'C'
        unfit_langs = list(map(lambda p: p[0], filter(lambda p: p[1] < lang_part_counts[default_lang],
                                                      lang_part_counts.items())))
        for lang in unfit_langs:
            self.object.pop(lang)
        for lang in self.object:
            self.object[lang] = self.object[lang].strip()

    def serialize(self):
        return self.object


class Artifact(Node):
    def __init__(self):
        self.type = ''
        self.platform = ''
        self.bundle = ''
        self.locations = []
        self.checksum = {}
        self.size = {}
        # self.filename = ''

    def parse_tree(self, node, lang_code_func=None):
        """ Parse a <artifact> object """
        self.type = node.get('type')
        self.platform = node.get('platform', '')
        self.bundle = node.get('bundle', '')
        for c4 in node:
            val = c4.text.strip()
            if c4.tag == 'location':
                self.locations.append(val)
            elif c4.tag == 'checksum':
                self.checksum[c4.get('type')] = val
            elif c4.tag == 'size':
                if c4.get('type') == 'download':
                    self.size['download'] = int(val)
                elif c4.get('type') == 'installed':
                    self.size['installed'] = int(val)


class Release(Node):
    NOT_TO_SERIALIZE = ['timestamp', 'date']

    def __init__(self):
        self.version = ''
        self.timestamp = 0
        self.date = ''
        self.unix_timestamp = 0
        # self.date_eol = ''
        # self.urgency = 'medium'
        self.type = 'stable'
        self.description = None
        self.url: dict[str, str] = {}
        # self.issues = []
        self.artifacts: list[Artifact] = []

    def parse_tree(self, node, lang_code_func=None):
        """ Parse a <release> object """
        if 'timestamp' in node.attrib:
            self.timestamp = int(node.attrib['timestamp'])
        if 'date' in node.attrib:
            self.date = node.get('date')
        if self.timestamp:
            self.unix_timestamp = self.timestamp
        elif self.date:  # 'timestamp' takes precedence over 'date'
            dt = dateutil.parser.parse(self.date)
            self.unix_timestamp = int(dt.strftime("%s"))
        if 'version' in node.attrib:
            self.version = node.attrib['version']
            # fix up hex value
            if self.version.startswith('0x'):
                self.version = str(int(self.version[2:], 16))
        self.type = node.get('type', 'stable')
        for c3 in node:
            if c3.tag == 'description':
                self.description = Description()
                self.description.parse_tree(c3, lang_code_func)
            elif c3.tag == 'url':
                t = c3.get('type', 'details')
                self.url = {t: c3.text.strip()}
            elif c3.tag == 'artifacts':
                for c4 in c3:
                    a = Artifact()
                    a.parse_tree(c4)
                    self.artifacts.append(a)

    def serialize(self):
        obj = {}
        for a, v in vars(self).items():
            if a not in type(self).NOT_TO_SERIALIZE and v:
                serial_a = 'unix-timestamp' if a == 'unix_timestamp' else a
                obj[serial_a] = self.description.serialize() if a == 'description' \
                    else [x.serialize() for x in self.artifacts] if a == 'artifacts' \
                    else v
        return obj


class Image(Node):
    NOT_TO_SERIALIZE = ['type']

    def __init__(self):
        self.type = ''
        self.width = 0
        self.height = 0
        # xml:lang
        self.url = ''

    def parse_tree(self, node, lang_code_func=None):
        """ Parse a <image> object """
        self.type = node.get('type', '')
        self.width = int(node.get('width', 0))
        self.height = int(node.get('height', 0))
        self.url = node.text.strip()


class Screenshot(Node):
    def __init__(self):
        self.default = False
        self.caption = {}
        self.thumbnails = []
        self.source = None
        self.environment = ''

    def parse_tree(self, node, lang_code_func=None):
        """ Parse a <screenshot> object """
        self.default = node.get('type', '') == 'default'
        self.environment = node.get('environment', '')
        for c3 in node:
            if c3.tag == 'caption':
                utils.localize(self.caption, c3, lang_code_func=lang_code_func)
            elif c3.tag == 'image':
                im = Image()
                im.parse_tree(c3)
                if im.type == 'thumbnail':
                    self.thumbnails.append(im)
                else:
                    self.source = im

    def serialize(self):
        obj = {}
        for a, v in vars(self).items():
            if a not in type(self).NOT_TO_SERIALIZE and v:
                serial_a = 'source-image' if a == 'source' else a
                obj[serial_a] = self.source.serialize() if a == 'source' \
                    else [x.serialize() for x in self.thumbnails] if a == 'thumbnails' \
                    else v
        # appstreamcli always includes 'thumbnails'
        if 'thumbnails' not in obj:
            obj['thumbnails'] = []
        # video
        return obj


class Provide(Node):
    TYPES = {
        'mediatype': 'mediatypes',
        'library': 'libraries',
        'font': 'fonts',
        'modalias': 'modalaliases',
        'firmware': 'firmwares',
        'python2': 'python2',
        'python3': 'python3',
        'dbus': 'dbus',
        'binary': 'binaries',
        'id': 'ids'
    }

    def __init__(self):
        for v in self.TYPES.values():
            setattr(self, v, [])

    def parse_tree(self, node, lang_code_func=None):
        """ Parse a <provide> object """
        for c2 in node:
            if c2.tag in self.TYPES:
                attr = self.TYPES[c2.tag]
                current = getattr(self, attr)
                if c2.tag == 'dbus':
                    if 'type' in c2.attrib and c2.get('type') in ['user', 'system']:
                        current.append({'type': c2.get('type'), 'service': c2.text.strip()})
                else:
                    current.append(c2.text.strip())
                setattr(self, attr, current)


class ContentRating(Node):
    def __init__(self):
        self.type = ''
        self.attributes = {}

    def parse_tree(self, node, lang_code_func=None):
        self.type = node.get('type', 'oars-1.0')
        for c2 in node:
            if c2.tag == 'content_attribute' and 'id' in c2.attrib:
                self.attributes[c2.get('id')] = c2.text.strip()

    def serialize(self):
        return {self.type: self.attributes}
