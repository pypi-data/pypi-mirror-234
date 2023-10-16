"""
:filename: test_status.py
:author:   Brigitte Bigi
:contact:  develop@sppas.org
:summary: Tests for HTTPD status in package httpd.

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

from whakerpy.httpd.hstatus import sppasHTTPDValueError
from whakerpy.httpd.hstatus import sppasHTTPDStatus

# ---------------------------------------------------------------------------


class TestHTTPDExceptions(unittest.TestCase):

    def test_status_value_errors(self):
        try:
            raise sppasHTTPDValueError("value")
        except ValueError as e:
            self.assertTrue(isinstance(e, sppasHTTPDValueError))
            self.assertTrue("0377" in str(e))
            self.assertEqual(377, e.status)

# ---------------------------------------------------------------------------


class TestHTTPDStatus(unittest.TestCase):

    def test_check(self):
        # Check success
        self.assertEqual(100, sppasHTTPDStatus.check(100))
        self.assertEqual(200, sppasHTTPDStatus.check("200"))

        # Check fail
        with self.assertRaises(sppasHTTPDValueError):
            sppasHTTPDStatus.check("AZERTY")
        with self.assertRaises(sppasHTTPDValueError):
            sppasHTTPDStatus.check(84)

    def test_init(self):
        s = sppasHTTPDStatus()
        self.assertEqual(str(s), "200")
        self.assertTrue(s == 200)
        self.assertEqual(200, s)

    def test_get_set(self):
        s = sppasHTTPDStatus()
        s.code = 404
        self.assertEqual(404, s)
        self.assertEqual(404, s.code)

        with self.assertRaises(sppasHTTPDValueError):
            s.code = "azerty"
        with self.assertRaises(sppasHTTPDValueError):
            s.code = 1974

    def test_str(self):
        s = sppasHTTPDStatus()
        self.assertEqual(str(s), "200")
        self.assertEqual(repr(s), "200: OK")
