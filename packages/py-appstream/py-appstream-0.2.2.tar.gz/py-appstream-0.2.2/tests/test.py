# SPDX-FileCopyrightText: 2022 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

import importlib.resources as pkg_resources
import unittest

from py_appstream.component import Component


class ComponentTestCase(unittest.TestCase):
    with pkg_resources.open_text('tests', 'test.appdata.xml') as f_xml:
        xml_data = f_xml.read()
        component = Component()
        component.parse_tree(xml_data)
        obj = component.serialize()
        # import json
        # with open('test.json', 'w') as f_json:
        #     json.dump(component.serialize(), f_json, ensure_ascii=False, indent=2)
        # import yaml
        # with open('test.yaml', 'w') as f_yaml:
        #     yaml.dump(component.serialize(), f_yaml, allow_unicode=True)

    def test_extends(self):
        extends = self.component.extends
        self.assertEqual('org.kde.krusader.desktop', extends[2])
        # serialization
        self.assertEqual(4, len(self.obj['Extends']))

    def test_description(self):
        desc = self.component.description
        self.assertEqual({'C', 'ca', 'ko'}, set(desc.object.keys()), 'Only fully translated languages are included')
        ca_parts = desc.object['ca'].split('>\n')
        conditions = (ca_parts[0].startswith('<p>') and ca_parts[6].startswith('<p>') and
                      ca_parts[2].startswith('  <li>') and ca_parts[3].startswith('  <li>') and
                      ca_parts[4].startswith('  <li>'))
        self.assertTrue(conditions, 'First and last parts are paragraphs, middle parts are list items')

    def test_releases(self):
        releases = self.component.releases
        release = releases[0]
        self.assertEqual(release.type, 'stable', 'default release type is stable')
        artifact = release.artifacts[0]
        self.assertEqual(len(artifact.locations), 1)
        self.assertEqual({'sha256', 'blake2b'}, set(artifact.checksum.keys()))
        # serialization
        self.assertIn('unix-timestamp', self.obj['Releases'][0])

    def test_screenshots(self):
        screenshots = self.component.screenshots
        self.assertTrue(screenshots[0].default)
        self.assertEqual({'C', 'de', 'ko', 'es', 'ca'}, set(screenshots[1].caption.keys()))
        # XML elements inside caption
        self.assertEqual('O l\'actiu La comunitat d\'artistes del Krita anchor', screenshots[2].caption['ca'])
        # Exclude empty string
        self.assertEqual({'C', 'ca'}, set(screenshots[2].caption.keys()))
        # environment attribute
        self.assertEqual('windows', self.component.screenshots[4].environment)
        # serialization
        self.assertIn('source-image', self.obj['Screenshots'][0])
        self.assertEqual('https://gcompris.net/screenshots_qt/large/color_mix.png',
                         self.obj['Screenshots'][3]['source-image']['url'])
        self.assertEqual('windows', self.obj['Screenshots'][4]['environment'])

    def test_provide(self):
        provide = self.component.provides
        self.assertEqual({'binaries', 'mediatypes', 'dbus'}, set([k for k, v in vars(provide).items() if v]))
        self.assertEqual(1, len(getattr(provide, 'binaries')))
        self.assertEqual(8, len(getattr(provide, 'mediatypes')))
        # only <dbus> tags with 'type' attribute of 'user' or 'system' are counted
        self.assertEqual(1, len(getattr(provide, 'dbus')))
        self.assertEqual('user', getattr(provide, 'dbus')[0]['type'])
        # serialization
        self.assertEqual({'binaries', 'mediatypes', 'dbus'}, set(self.obj['Provides'].keys()))

    def test_content_rating(self):
        content_rating = self.component.content_rating
        self.assertEqual('oars-1.1', content_rating.type)
        self.assertEqual(2, len(content_rating.attributes.keys()))
        # serialization
        self.assertEqual(2, len(self.obj['ContentRating']['oars-1.1'].keys()))

    def test_icon(self):
        icon = self.component.icon
        self.assertEqual({'stock', 'remote', 'local', 'cached'}, set(icon.keys()))
        self.assertEqual('web-browser', icon['stock'])
        self.assertEqual(2, len(icon['remote']))
        self.assertEqual(2, len(icon['cached']))
        self.assertEqual('/usr/share/pixmaps/foobar.png', icon['local'][-1]['name'])

    def test_component(self):
        self.assertEqual('desktop-application', self.component.type)
        self.assertEqual('KDE', self.component.project_group)
        self.assertEqual(5, len(self.component.name.keys()))
        self.assertEqual({}, self.component.developer_name)
        self.assertEqual(5, len(self.component.screenshots))
        self.assertEqual(3, len(self.component.releases))
        # serialization
        self.assertEqual(17, len(self.obj.keys()))
        self.assertEqual(4, len(self.obj['Keywords']['C']))


if __name__ == '__main__':
    unittest.main()
