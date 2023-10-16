"""
:filename: test_htree.py
:author:   Brigitte Bigi
:contact:  develop@sppas.org
:summary: Tests for HTMLTree in package htmlmaker.

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

from whakerpy.htmlmaker.hexc import NodeChildTagError
from whakerpy.htmlmaker.emptynodes import EmptyNode
from whakerpy.htmlmaker.tagnodes import HTMLNode

from whakerpy.htmlmaker.treeelts import HTMLHeadNode
from whakerpy.htmlmaker.treenode import HTMLTree

# ---------------------------------------------------------------------------


class TestHeadNode(unittest.TestCase):

    def test_init(self):
        node = HTMLHeadNode(parent=None)
        self.assertEqual("head", node.identifier)

    def test_error(self):
        node = HTMLHeadNode(parent=None)
        with self.assertRaises(NodeChildTagError):
            node.append_child(HTMLNode(parent=node.identifier, identifier=None, tag="p"))

    def test_append(self):
        node = HTMLHeadNode(parent=None)
        child_node = EmptyNode(node.identifier, None, "meta")
        node.append_child(child_node)
        with self.assertRaises(NodeChildTagError):
            node.append_child(EmptyNode(node.identifier, None, "img"))

    def test_insert(self):
        node = HTMLHeadNode(parent=None)
        child_node = EmptyNode(node.identifier, None, "meta")
        node.insert_child(1, child_node)
        with self.assertRaises(NodeChildTagError):
            node.insert_child(0, EmptyNode(node.identifier, None, "img"))

    def test_title(self):
        pass

    def test_meta(self):
        pass

    def test_link(self):
        pass

    def test_script(self):
        pass

    def test_css(self):
        pass

# ---------------------------------------------------------------------------


class TestTree(unittest.TestCase):

    def test_init(self):
        tree = HTMLTree("home")
        self.assertTrue(tree.is_root())
        self.assertFalse(tree.is_leaf())
        self.assertTrue(tree.has_child("html"))
        self.assertIsInstance(tree.head, HTMLNode)
        self.assertIsInstance(tree._get_body(), HTMLNode)
        self.assertIsInstance(tree.body_header, HTMLNode)
        self.assertIsInstance(tree.body_main, HTMLNode)
        self.assertIsInstance(tree.body_footer, HTMLNode)

        self.assertEqual(tree.body_header.identifier, "body_header")
        self.assertEqual(tree.body_main.identifier, "body_main")
        self.assertEqual(tree.body_footer.identifier, "body_footer")

    def test_add_html_attribute(self):
        tree = HTMLTree("home")
        tree.add_html_attribute("lang", "en")
        self.assertEqual(tree._HTMLTree__html.get_attribute_value("lang"), "en")
        with self.assertRaises(TypeError):
            tree.add_html_attribute("lang", 3)
        with self.assertRaises(ValueError):
            # NodeAttributeError.
            # The attribute can't be assigned to this element.
            tree.add_html_attribute("language", "en")

    def test_add_body_attribute(self):
        tree = HTMLTree("home")
        tree.add_body_attribute("class", "container")
        self.assertEqual(tree.get_body_attribute_value("class"), "container")

    def test_set_body_attribute(self):
        tree = HTMLTree("home")
        tree.set_body_attribute("id", "main-content")
        self.assertEqual(tree.get_body_attribute_value("id"), "main-content")

    def test_set_head(self):
        tree = HTMLTree("home")
        head_node = HTMLNode(tree.identifier, "head", "head")
        tree.set_head(head_node)
        self.assertIs(tree.get_head(), head_node)

    def test_set_parent(self):
        tree = HTMLTree("home")
        # create a div with no parent
        node = HTMLNode(None, None, 'div')
        # set the parent to the div
        node.set_parent(tree.body_header.identifier)
        self.assertTrue(node.get_parent() is tree.body_header.identifier)
        # append the div to the tree
        tree.body_header.append_child(node)

    def test_serialize(self):
        value = """<!DOCTYPE html>

<html>
    <head></head>
<body>
    <main></main>

</body>
</html>
"""
        tree = HTMLTree("home")
        self.assertEqual("HTMLTree (home)", str(tree))
        self.assertEqual(tree.serialize(), value)
        self.assertEqual(value, repr(tree))
