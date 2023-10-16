"""
:filename: test_hexc.py
:author:   Brigitte Bigi
:contact:  develop@sppas.org
:summary:  Tests for exceptions in package whakerpy.htmlmaker.

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

from whakerpy.htmlmaker.hexc import NodeTypeError
from whakerpy.htmlmaker.hexc import NodeInvalidIdentifierError
from whakerpy.htmlmaker.hexc import NodeTagError
from whakerpy.htmlmaker.hexc import NodeChildTagError
from whakerpy.htmlmaker.hexc import NodeKeyError
from whakerpy.htmlmaker.hexc import NodeIdentifierError
from whakerpy.htmlmaker.hexc import NodeAttributeError
from whakerpy.htmlmaker.hexc import NodeParentIdentifierError

# ---------------------------------------------------------------------------


class TestExceptions(unittest.TestCase):

    def test_node_errors(self):
        try:
            raise NodeTypeError(None)
        except TypeError as e:
            self.assertTrue(isinstance(e, NodeTypeError))
            self.assertTrue("9110" in str(e))
            self.assertEqual(9110, e.status)

        try:
            raise NodeInvalidIdentifierError("invalid identifier")
        except ValueError as e:
            self.assertTrue(isinstance(e, NodeInvalidIdentifierError))
            self.assertTrue("9310" in str(e))
            self.assertEqual(9310,  e.status)

        try:
            raise NodeParentIdentifierError("invalid identifier", "expected one")
        except ValueError as e:
            self.assertTrue(isinstance(e, NodeParentIdentifierError))
            self.assertTrue(isinstance(e, ValueError))
            self.assertTrue("9312" in str(e))
            self.assertEqual(9312,  e.status)

        try:
            raise NodeTagError("invalid tag")
        except ValueError as e:
            self.assertTrue(isinstance(e, NodeTagError))
            self.assertTrue("9320" in str(e))
            self.assertEqual(9320, e.status)

        try:
            raise NodeChildTagError("invalid child tag")
        except ValueError as e:
            self.assertTrue(isinstance(e, NodeChildTagError))
            self.assertTrue("9325" in str(e))
            self.assertEqual(9325, e.status)

        try:
            raise NodeAttributeError("invalid child tag")
        except ValueError as e:
            self.assertTrue(isinstance(e, NodeAttributeError))
            self.assertTrue(isinstance(e, ValueError))
            self.assertTrue("9330" in str(e))
            self.assertEqual(9330, e.status)

        try:
            raise NodeKeyError("data name", "key")
        except KeyError as e:
            self.assertTrue(isinstance(e, NodeKeyError))
            self.assertTrue("9400" in str(e))
            self.assertEqual(9400, e.status)

        try:
            raise NodeIdentifierError("data name", "key")
        except KeyError as e:
            self.assertTrue(isinstance(e, NodeIdentifierError))
            self.assertTrue(isinstance(e, KeyError))
            self.assertTrue("9410" in str(e))
            self.assertEqual(9410, e.status)
