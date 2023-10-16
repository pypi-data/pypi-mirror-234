# SPDX-FileCopyrightText: 2022 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

from __future__ import annotations

from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError

from . import utils
from .exceptions import AppStreamParseError
from .subcomponent import Node, Description, Release, Provide, Screenshot, ContentRating


class Component(Node):
    NOT_TO_SERIALIZE = ['metadata_license', 'update_contact']
    JUST_TEXT = ['id', 'metadata_license', 'project_group', 'project_license', 'update_contact']
    TO_LOCALIZE = ['name', 'summary', 'developer_name']
    TO_PARSE_TREE = {
        'description': Description,
        'provides': Provide,
        'content_rating': ContentRating
    }
    TO_LIST = {
        'releases': {'singular': 'release', 'class': Release},
        'screenshots': {'singular': 'screenshot', 'class': Screenshot}
    }
    SERIAL_NAMES = {
        'id': 'ID',
        'pkgname': 'Package'
    }

    def __init__(self):
        self.type = ''
        # date_eol
        self.id = ''
        self.metadata_license = ''
        self.name = {}
        self.summary = {}
        self.icon = {}
        self.description = None
        self.categories = []
        self.url = {}
        self.launchable = {}
        self.releases: list[Release] = []
        self.provides = None
        # recommends, supports
        self.project_group = ''
        # compulsory_for_desktop
        self.project_license = ''
        self.developer_name = {}
        self.screenshots: list[Screenshot] = []
        # translation, suggests
        self.content_rating = None
        # agreement
        self.update_contact = ''
        # name_variant_suffix, branding, tags
        self.custom = {}
        # collection metadata
        self.pkgname = ''
        self.keywords = {}
        # languages, bundle
        self.extends = []

    def parse_tree(self, node, lang_code_func=None, drop_desktop_id=False):
        if isinstance(node, str):
            try:
                root = ElementTree.fromstring(node)
            except ParseError as e:
                raise AppStreamParseError(str(e))
        else:
            root = node

        self.type = root.attrib.get('type', '')
        if self.type == 'desktop':
            self.type = 'desktop-application'
        for c1 in root:
            val = c1.text.strip() if c1.text else ''
            if c1.tag in self.JUST_TEXT:
                if c1.tag == 'id':
                    val = val.replace('.desktop', '') if drop_desktop_id else val
                setattr(self, c1.tag, val)
            elif c1.tag in self.TO_LOCALIZE:
                utils.localize(getattr(self, c1.tag), c1, lang_code_func=lang_code_func)
            elif c1.tag in self.TO_PARSE_TREE:
                setattr(self, c1.tag, self.TO_PARSE_TREE[c1.tag]())
                (getattr(getattr(self, c1.tag), 'parse_tree'))(c1, lang_code_func=lang_code_func)
            elif c1.tag in self.TO_LIST:
                for c2 in c1:
                    if c2.tag == self.TO_LIST[c1.tag]['singular']:
                        o = self.TO_LIST[c1.tag]['class']()
                        o.parse_tree(c2, lang_code_func=lang_code_func)
                        (getattr(getattr(self, c1.tag), 'append'))(o)
            elif c1.tag == 'icon':
                t = c1.get('type')
                if t == 'stock':
                    self.icon[t] = val
                elif t in ['cached', 'local', 'remote']:
                    if t not in self.icon:
                        self.icon[t] = []
                    icon_obj = {}
                    for k in ['width', 'height', 'scale']:
                        if k in c1.attrib:
                            icon_obj[k] = int(c1.get(k))
                    k = 'url' if t == 'remote' else 'name'
                    icon_obj[k] = val
                    self.icon[t].append(icon_obj)
            elif c1.tag == 'categories':
                for c2 in c1:
                    if c2.tag == 'category':
                        self.categories.append(c2.text.strip())
            elif c1.tag == 'url':
                k = c1.attrib.get('type', 'homepage')
                self.url[k] = val
            elif c1.tag == 'launchable':
                t = c1.get('type')
                if t not in self.launchable:
                    self.launchable[t] = []
                if t == 'desktop-id':
                    val = val.replace('.desktop', '') if drop_desktop_id else val
                self.launchable[t].append(val)
            elif c1.tag == 'custom':
                for c2 in c1:
                    if c2.tag == 'value' and 'key' in c2.attrib:
                        self.custom[c2.get('key')] = c2.text.strip()
            elif c1.tag == 'pkgname':
                self.pkgname = val
            elif c1.tag == 'keywords':
                lang = c1.get('{http://www.w3.org/XML/1998/namespace}lang', c1.attrib.get('lang', 'C'))
                kw = []
                for c2 in c1:
                    if c2.tag == 'keyword':
                        kw.append(c2.text.strip())
                self.keywords[lang] = kw
            elif c1.tag == 'extends':
                val = val.replace('.desktop', '') if drop_desktop_id else val
                self.extends.append(val)

    def serialize(self):
        obj = {}
        for k, v in vars(self).items():
            if k not in type(self).NOT_TO_SERIALIZE and v:
                serial_k = self.SERIAL_NAMES[k] if k in self.SERIAL_NAMES \
                    else ''.join(map(lambda x: x.capitalize(), k.split('_')))
                obj[serial_k] = self.content_rating.serialize() if k == 'content_rating' \
                    else [x.serialize() for x in self.releases] if k == 'releases' \
                    else self.description.serialize() if k == 'description' \
                    else self.provides.serialize() if k == 'provides' \
                    else [x.serialize() for x in self.screenshots] if k == 'screenshots' \
                    else v
        return obj
