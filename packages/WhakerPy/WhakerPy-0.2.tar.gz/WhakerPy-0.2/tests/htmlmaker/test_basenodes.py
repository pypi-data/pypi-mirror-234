"""
:filename: test_basenodes.py
:author:   Brigitte Bigi
:contact:  develop@sppas.org
:summary: Tests for HTML base nodes in package htmlmaker.

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

from whakerpy.htmlmaker.hexc import NodeInvalidIdentifierError
from whakerpy.htmlmaker.hexc import NodeKeyError

from whakerpy.htmlmaker.basenodes import BaseNode
from whakerpy.htmlmaker.basenodes import HTMLComment
from whakerpy.htmlmaker.basenodes import Doctype

# ---------------------------------------------------------------------------


class TestBaseNode(unittest.TestCase):

    def test_init_successfully(self):
        # Default identifier and default parent
        node = BaseNode()
        self.assertIsNotNone(node.identifier)
        self.assertIsInstance(node, BaseNode)
        self.assertEqual(36, len(node.identifier))
        self.assertTrue(node.is_leaf())
        self.assertTrue(node.is_root())
        self.assertFalse(node.has_child("lol"))
        self.assertIsNone(node.get_parent())

        # Custom identifier and default parent
        node = BaseNode(parent=None, identifier="toto")
        self.assertEqual("toto", node.identifier)

        # Custom identifier and custom parent
        node = BaseNode(parent="dad", identifier="toto")
        self.assertEqual("dad", node.get_parent())
        self.assertEqual("toto", node.identifier)

        # Custom parent and default identifier
        node = BaseNode(parent="dad")
        self.assertEqual("dad", node.get_parent())
        self.assertEqual(36, len(node.identifier))

    # -----------------------------------------------------------------------

    def test_init_errors(self):
        with self.assertRaises(NodeInvalidIdentifierError):
            BaseNode(parent=None, identifier="")

        with self.assertRaises(NodeInvalidIdentifierError):
            BaseNode(parent=None, identifier="  ")

        with self.assertRaises(NodeInvalidIdentifierError):
            BaseNode(parent=None, identifier="my id")

        with self.assertRaises(NodeInvalidIdentifierError):
            BaseNode(parent=None, identifier=" my_id")

        with self.assertRaises(NodeKeyError):
            BaseNode(parent="dad", identifier="dad")

    # -----------------------------------------------------------------------

    def test_validate_identifier(self):
        # Check identifier validation
        with self.assertRaises(NodeInvalidIdentifierError):
            # Empty identifier should raise an exception
            BaseNode.validate_identifier("")

        with self.assertRaises(NodeInvalidIdentifierError):
            # Identifier with space should raise an exception
            BaseNode.validate_identifier(" ")

        # Valid identifier should not raise an exception
        self.assertEqual(BaseNode.validate_identifier("valid_id"), "valid_id")

    # -----------------------------------------------------------------------

    def test_is_leaf(self):
        node1 = BaseNode()
        node2 = BaseNode(identifier="test_id")
        node3 = BaseNode(parent="parent_id", identifier="test_id")
        # Check if node is a leaf (should always be true for BaseNode)
        self.assertTrue(node1.is_leaf())
        self.assertTrue(node2.is_leaf())
        self.assertTrue(node3.is_leaf())

    # -----------------------------------------------------------------------

    def test_is_root(self):
        node1 = BaseNode()
        node2 = BaseNode(identifier="test_id")
        node3 = BaseNode(parent="parent_id", identifier="test_id")
        # Check if node is a root (should be true only for node1)
        self.assertTrue(node1.is_root())
        self.assertTrue(node2.is_root())
        self.assertFalse(node3.is_root())

    # -----------------------------------------------------------------------

    def test_get_set_parent(self):
        node1 = BaseNode()
        node3 = BaseNode(parent="parent_id", identifier="test_id")
        # Check getter and setter for parent
        self.assertIsNone(node1.get_parent())
        self.assertEqual(node3.get_parent(), "parent_id")

        node1.set_parent("new_parent_id")
        self.assertEqual(node1.get_parent(), "new_parent_id")

        # Check that the setter raises an exception when the
        # parent's identifier is the same as the node's identifier
        with self.assertRaises(NodeKeyError):
            node1.set_parent(node1.identifier)

    # -----------------------------------------------------------------------

    def test_has_child(self):
        node1 = BaseNode()
        node2 = BaseNode(identifier="parent_id")
        node3 = BaseNode(parent="parent_id", identifier="test_id")
        # Check that has_child returns True for node3 (as it has a parent)
        self.assertFalse(node3.has_child(node1.identifier))
        self.assertFalse(node1.has_child(node2.identifier))
        self.assertFalse(node2.has_child(node3.identifier))

    def test_serialize(self):
        self.assertEqual("", BaseNode().serialize())

# ---------------------------------------------------------------------------


class TestElements(unittest.TestCase):

    def test_doctype(self):
        d = Doctype()
        self.assertEqual('<!DOCTYPE html>\n\n', d.serialize())

    def test_comment(self):
        c = HTMLComment("parent_id", "this is a comment")
        self.assertEqual('\n<!-- -------------------------- this is a comment -------------------------- -->\n\n',
                         c.serialize(nbs=0))
