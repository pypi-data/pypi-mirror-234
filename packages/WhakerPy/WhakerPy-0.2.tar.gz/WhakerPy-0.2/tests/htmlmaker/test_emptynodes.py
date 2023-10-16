"""
:filename: test_emptynodes.py
:author:   Brigitte Bigi
:contact:  develop@sppas.org
:summary: Tests for HTML empty nodes in package htmlmaker.

.. _This file is part of SPPAS: https://sppas.org/
..
    -------------------------------------------------------------------------

     ___   __    __    __    ___
    /     |  \  |  \  |  \  /              the automatic
    \__   |__/  |__/  |___| \__             annotation and
       \  |     |     |   |    \             analysis
    ___/  |     |     |   | ___/              of speech

    Copyright (C) 2011-2023 Brigitte Bigi
    Laboratoire Parole et Langage, Aix-en-Provence, France

    Use of this software is governed by the GNU Public License, version 3.

    SPPAS is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SPPAS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SPPAS. If not, see <http://www.gnu.org/licenses/>.

    This banner notice must not be removed.

    -------------------------------------------------------------------------

"""

import unittest

from whakerpy.htmlmaker import NodeAttributeError
from whakerpy.htmlmaker import NodeTagError
from whakerpy.htmlmaker import NodeKeyError

from whakerpy.htmlmaker.basenodes import BaseNode
from whakerpy.htmlmaker.emptynodes import EmptyNode
from whakerpy.htmlmaker.emptynodes import HTMLHr
from whakerpy.htmlmaker.emptynodes import HTMLImage

# ---------------------------------------------------------------------------


class TestEmptyNode(unittest.TestCase):

    def test_init_successfully(self):
        node = EmptyNode(None, None, "br")
        self.assertEqual(36, len(node.identifier))
        self.assertTrue(node.is_leaf())
        self.assertTrue(node.is_root())
        self.assertFalse(node.has_child("lol"))
        self.assertIsNone(node.get_parent())
        self.assertEqual(0, node.nb_attributes())

        node = EmptyNode(None, None, "img", {"src": "path/file"})
        self.assertEqual(1, node.nb_attributes())

    # -----------------------------------------------------------------------

    def test_check_attribute(self):
        # Wrong type
        with self.assertRaises(NodeAttributeError):
            e = EmptyNode(None, None, "img")
            e.check_attribute(BaseNode())

        # Unknown attribute
        with self.assertRaises(NodeAttributeError):
            e = EmptyNode(None, None, "img")
            e.check_attribute("toto")

        e = EmptyNode(None, None, "img")
        self.assertTrue(e.check_attribute("src"))
        self.assertTrue(e.check_attribute("alt"))
        self.assertTrue(e.check_attribute("loop"))  # but should be False

    # -----------------------------------------------------------------------

    def test_init_errors(self):
        with self.assertRaises(NodeTagError):
            EmptyNode(None, None, "invented")

        with self.assertRaises(TypeError):
            EmptyNode(None, None, "img", "src")

        with self.assertRaises(ValueError):
            EmptyNode(None, None, "img", {"key": "value"})

    # -----------------------------------------------------------------------

    def test_tag(self):
        # Check if tag property returns the correct tag
        empty_node = EmptyNode("parent_id", "test_id", "a", {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(empty_node.tag, "a")

    # -----------------------------------------------------------------------

    def test_add_attribute(self):
        empty_node = EmptyNode("parent_id", "test_id", "a", {"href": "https://example.com", "target": "_blank"})
        # Check if add_attribute method adds the attribute correctly
        empty_node.add_attribute("rel", "nofollow")
        self.assertTrue(empty_node.has_attribute("rel"))
        self.assertEqual(empty_node.get_attribute_value("rel"), "nofollow")

        # Add another one
        empty_node.add_attribute("required", None)
        self.assertTrue(empty_node.has_attribute("required"))
        self.assertEqual(empty_node.get_attribute_value("required"), None)
        # Set the value to an existing un-valued attribute
        empty_node.add_attribute("required", "true")
        self.assertEqual(empty_node.get_attribute_value("required"), "true")

        # Add another one
        empty_node.add_attribute("class", "nice")
        self.assertTrue(empty_node.has_attribute("class"))
        self.assertEqual(empty_node.get_attribute_value("class"), "nice")
        # Append a new value to an existing attribute
        empty_node.add_attribute("class", "pretty")
        self.assertEqual(empty_node.get_attribute_value("class"), "nice pretty")

    def test_remove_attribute(self):
        empty_node = EmptyNode("parent_id", "test_id", "a", {"href": "https://example.com", "target": "_blank"})

        empty_node.add_attribute("required", None)
        empty_node.remove_attribute("required")
        self.assertFalse(empty_node.has_attribute("rel"))

        empty_node.add_attribute("class", "nice")
        empty_node.remove_attribute("class")
        self.assertFalse(empty_node.has_attribute("class"))

    def test_get_set_attribute(self):
        empty_node = EmptyNode("parent_id", "test_id", "a", {"href": "https://example.com", "target": "_blank"})
        # Check if set_attribute method sets the attribute correctly and replaces existing one
        empty_node.set_attribute("href", "https://example.org")
        self.assertEqual(empty_node.get_attribute_value("href"), "https://example.org")
        # Check if get_attribute_keys method returns the list of attribute keys
        self.assertEqual(empty_node.get_attribute_keys(), ["href", "target"])

        # Attribute values given as list
        empty_node.set_attribute("class", ["nice", "pretty"])
        self.assertEqual(empty_node.get_attribute_value("class"), "nice pretty")

    def test_has_attribute(self):
        empty_node = EmptyNode("parent_id", "test_id", "a", {"href": "https://example.com", "target": "_blank"})
        # Check if has_attribute method returns True for existing attribute, False otherwise
        self.assertTrue(empty_node.has_attribute("href"))
        self.assertFalse(empty_node.has_attribute("class"))

    def test_remove_attribute(self):
        empty_node = EmptyNode("parent_id", "test_id", "a", {"href": "https://example.com", "target": "_blank"})
        # Check if remove_attribute method removes the attribute correctly
        empty_node.remove_attribute("href")
        self.assertFalse(empty_node.has_attribute("href"))

    def test_remove_attribute_value(self):
        empty_node = EmptyNode("parent_id", "test_id", "a", {"href": "https://example.com", "target": "_blank"})
        # Check if remove_attribute_value method removes the value from the attribute correctly
        empty_node.add_attribute("class", "active selected")
        empty_node.remove_attribute_value("class", "active")
        self.assertTrue(empty_node.has_attribute("class"))
        self.assertEqual(empty_node.get_attribute_value("class"), "selected")

    def test_nb_attributes(self):
        empty_node = EmptyNode("parent_id", "test_id", "a", {"href": "https://example.com", "target": "_blank"})
        # Check if nb_attributes method returns the correct number of attributes
        self.assertEqual(empty_node.nb_attributes(), 2)

    def test_browse_attributes(self):
        node = EmptyNode(None, None, "img", {"src": "path/file"})
        self.assertEqual(1, len(node.get_attribute_keys()))
        node.add_attribute("alt", "")
        self.assertEqual(2, len(node.get_attribute_keys()))

    # -----------------------------------------------------------------------

    def test_serialize(self):
        empty_node = EmptyNode("parent_id", "test_id", "a", {"href": "https://example.com", "target": "_blank"})
        # Check if serialize method generates the correct HTML string
        expected_html = '    <a href="https://example.com" target="_blank" />\n'
        self.assertEqual(empty_node.serialize(), expected_html)


# ---------------------------------------------------------------------------


class TestElements(unittest.TestCase):

    def test_image(self):
        i = HTMLImage("parent_id", "img_id", src="/path/to/image.png")
        self.assertTrue(i.has_attribute("src"))
        self.assertTrue(i.has_attribute("alt"))

    def test_hr(self):
        hr = HTMLHr("parent_id")
        hr.set_attribute("class", "nidehr")
        self.assertTrue(hr.has_attribute("class"))
        with self.assertRaises(NodeAttributeError):
            hr.set_attribute("required", None)
