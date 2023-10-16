"""
:filename: test_tagnodes.py
:author:   Brigitte Bigi
:contact:  develop@sppas.org
:summary: Tests for HTML tag nodes in package htmlmaker.

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

from whakerpy.htmlmaker import NodeTagError
from whakerpy.htmlmaker import NodeKeyError

from whakerpy.htmlmaker.basenodes import BaseNode
from whakerpy.htmlmaker.tagnodes import HTMLNode
from whakerpy.htmlmaker.tagnodes import HTMLInputText
from whakerpy.htmlmaker.tagnodes import HTMLRadioBox
from whakerpy.htmlmaker.tagnodes import HTMLButtonNode

# ---------------------------------------------------------------------------


class TestTagNode(unittest.TestCase):

    def test_init_successfully(self):
        HTMLNode(parent=None, identifier="id01", tag="p")

    def test_init_error(self):
        with self.assertRaises(NodeTagError):
            HTMLNode(parent=None, identifier="id01", tag="tag")

    # -----------------------------------------------------------------------

    def test_has_child(self):
        node1 = BaseNode()
        node2 = HTMLNode(parent=None, identifier="parent_id", tag="p")
        node3 = BaseNode(parent="parent_id", identifier="test_id")
        node2.append_child(node3)
        # Check that has_child returns True for node3 (as it has a parent)
        self.assertFalse(node3.has_child(node1.identifier))
        self.assertFalse(node1.has_child(node2.identifier))
        self.assertTrue(node2.has_child(node3.identifier))

    # -----------------------------------------------------------------------

    def test_get_child(self):
        pnode = HTMLNode(parent=None, identifier="parent_id", tag="p")
        cnode = HTMLNode(parent=pnode.identifier, identifier="child", tag="p")

        # get child from its identifier
        self.assertIsNone(pnode.get_child(cnode))
        self.assertIsNone(pnode.get_child(cnode.identifier))
        pnode.append_child(cnode)
        self.assertIs(cnode, pnode.get_child("child"))

        # get child from its index
        self.assertIs(cnode, pnode.get_nidx_child(0))
        with self.assertRaises(IndexError):
            pnode.get_nidx_child(1)

    # -----------------------------------------------------------------------

    def test_append_child(self):
        pnode = HTMLNode(parent=None, identifier="parent", tag="div")
        cnode = HTMLNode(parent=pnode.identifier, identifier="child", tag="p")

        # Append a child into the node
        self.assertEqual(0, pnode.children_size())
        pnode.append_child(cnode)
        self.assertEqual(1, pnode.children_size())
        # Append the same child twice... nothing is done, silently.
        pnode.append_child(cnode)
        self.assertEqual(1, pnode.children_size())

        # test raised exceptions
        with self.assertRaises(NodeKeyError):
            pnode.append_child(pnode)
        with self.assertRaises(NodeKeyError):
            cnode.append_child(pnode)
        with self.assertRaises(TypeError):
            cnode.append_child(pnode.identifier)

    # -----------------------------------------------------------------------

    def test_insert_child(self):
        pnode = HTMLNode(parent=None, identifier="parent", tag="div")
        cnode = HTMLNode(parent=pnode.identifier, identifier="child", tag="p")
        anode = HTMLNode(parent="another_parent", identifier="child", tag="p")

        # Insert a child into the node
        self.assertEqual(0, pnode.children_size())
        pnode.insert_child(0, cnode)
        self.assertEqual(1, pnode.children_size())

        # test raised exceptions
        with self.assertRaises(NodeKeyError):
            pnode.insert_child(0, pnode)
        with self.assertRaises(NodeKeyError):
            cnode.insert_child(0, pnode)
        with self.assertRaises(TypeError):
            cnode.insert_child(0, pnode.identifier)

    # -----------------------------------------------------------------------

    def test_remove_child(self):
        pnode = HTMLNode(parent=None, identifier="parent", tag="div")
        cnode = HTMLNode(parent=pnode.identifier, identifier="childc", tag="p")
        anode = HTMLNode(parent=pnode.identifier, identifier="childa", tag="p")
        pnode.append_child(cnode)
        pnode.insert_child(0, anode)
        self.assertEqual(2, pnode.children_size())

        # Remove non existing child. do nothing silently.
        self.assertIsNone(pnode.remove_child("children"))
        # Remove child
        self.assertIsNone(pnode.remove_child("childa"))
        self.assertEqual(1, pnode.children_size())
        self.assertTrue(pnode.has_child("childc"))
        self.assertFalse(pnode.has_child("childa"))
        # Pop child
        with self.assertRaises(IndexError):
            pnode.pop_child(12)
        self.assertEqual(1, pnode.children_size())
        self.assertIsNone(pnode.pop_child(0))

    # -----------------------------------------------------------------------

    def test_various(self):
        pnode = HTMLNode(parent=None, identifier="parent", tag="div")
        self.assertTrue(pnode.is_root())
        self.assertTrue(pnode.is_leaf())
        cnode = HTMLNode(parent=pnode.identifier, identifier="childc", tag="p")
        self.assertFalse(cnode.is_root())
        anode = HTMLNode(parent=pnode.identifier, identifier="childa", tag="p")
        pnode.append_child(cnode)
        pnode.insert_child(0, anode)
        self.assertEqual(2, pnode.children_size())
        self.assertFalse(pnode.is_leaf())
        pnode.clear_children()
        self.assertEqual(0, pnode.children_size())
        self.assertTrue(pnode.is_leaf())

    # -----------------------------------------------------------------------

    def test_attribute(self):
        node = HTMLNode(parent=None, identifier="id01", tag="p")
        self.assertFalse(node.has_attribute("class"))
        self.assertIsNone(node.get_attribute_value("class"))

        node.add_attribute("class", None)
        self.assertTrue(node.has_attribute("class"))
        self.assertIsNone(node.get_attribute_value("class"))

        node.set_attribute("class", "toto")
        self.assertTrue(node.has_attribute("class"))
        self.assertEqual(node.get_attribute_value("class"), "toto")

        node.add_attribute("class", "titi")
        self.assertEqual(node.get_attribute_value("class"), "toto titi")

        node.set_attribute("class", "tata")
        self.assertEqual(node.get_attribute_value("class"), "tata")

    def test_value(self):
        node = HTMLNode(parent=None, identifier="id01", tag="p")
        self.assertIsNone(node.get_value())

        node.set_value("text")
        self.assertEqual("text", node.get_value())

        node.set_value(3)
        self.assertEqual("3", node.get_value())

# ---------------------------------------------------------------------------


class TestElements(unittest.TestCase):

    def test_init_tags(self):
        node = HTMLInputText(parent="parent_id", identifier="input0")
        self.assertTrue(node.has_attribute("type"))
        self.assertEqual("text", node.get_attribute_value("type"))
        self.assertEqual("input0", node.get_attribute_value("id"))
        self.assertEqual("input0", node.get_attribute_value("name"))

        node = HTMLRadioBox(parent="parent_id", identifier="radiobox")
        self.assertEqual("POST", node.get_attribute_value("method"))
        self.assertEqual("radiobox", node.get_attribute_value("id"))
        self.assertEqual("radiobox", node.get_attribute_value("name"))

        node1 = HTMLButtonNode(parent="parent_id", identifier="button1")
        self.assertEqual("button", node1.get_attribute_value("type"))
        self.assertEqual("button1", node1.get_attribute_value("id"))
        self.assertEqual("button1", node1.get_attribute_value("name"))

        node2 = HTMLButtonNode(parent="parent_id", identifier="button2", attributes={"type": "submit"})
        self.assertEqual("submit", node2.get_attribute_value("type"))
        self.assertEqual("button2", node2.get_attribute_value("id"))
        self.assertEqual("button2", node2.get_attribute_value("name"))

        node3 = HTMLButtonNode(parent="parent_id", identifier="button3", attributes={"id": "but3"})
        self.assertEqual("button", node3.get_attribute_value("type"))
        self.assertEqual("but3", node3.get_attribute_value("id"))
        self.assertEqual("button3", node3.get_attribute_value("name"))

        node4 = HTMLButtonNode(parent="parent_id", identifier="button4", attributes={"name": "but4"})
        self.assertEqual("button", node4.get_attribute_value("type"))
        self.assertEqual("button4", node4.get_attribute_value("id"))
        self.assertEqual("but4", node4.get_attribute_value("name"))

    # -----------------------------------------------------------------------

    def test_input(self):
        node = HTMLInputText(parent="parent_id", identifier="input0")
        node.set_name("newname")
        self.assertEqual("newname", node.get_attribute_value("name"))

    def test_radiobox(self):
        node = HTMLRadioBox(parent="parent_id", identifier="radiobox")
        node.append_input("nice", "Input value", "Input text", checked=False)
        self.assertEqual(1, node.children_size())

    def test_button(self):
        node = HTMLButtonNode(parent="parent_id", identifier="button")
        node.set_text("button_text", "Click me")
        self.assertEqual(1, node.children_size())
        node.set_icon("/path/to/icon.png")
        self.assertEqual(2, node.children_size())

