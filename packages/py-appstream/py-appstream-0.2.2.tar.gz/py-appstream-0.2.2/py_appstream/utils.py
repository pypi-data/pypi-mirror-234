# SPDX-FileCopyrightText: 2022 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

from xml.etree import ElementTree


def localize(out_obj, node, f=None, lang_code_func=None):
    lang = node.get('{http://www.w3.org/XML/1998/namespace}lang', node.get('lang', 'C'))
    if lang != 'x-test':
        val = ElementTree.tostring(node, encoding='unicode', method='text').strip()
        if val:
            lang = lang_code_func(lang) if lang_code_func else lang
            out_obj[lang] = f(val) if f else val


def join_lines(txt: str):
    return ' '.join(txt.replace('\n', ' ').split())
