# -*- coding: UTF-8 -*-
"""
:filename: sppas.ui.whakerpy.httpd.hstatus.py
:author:   Brigitte Bigi
:contact:  develop@sppas.org
:summary:  The HTTPD status codes.

.. _This file is part of SPPAS: https://sppas.org/
..
    -------------------------------------------------------------------------

     ___   __    __    __    ___
    /     |  \  |  \  |  \  /              the automatic
    \__   |__/  |__/  |___| \__             annotation and
       \  |     |     |   |    \             analysis
    ___/  |     |     |   | ___/              of speech

    Copyright (C) 2011-2023  Brigitte Bigi
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

from whakerpy.messages import error

# -----------------------------------------------------------------------


class sppasHTTPDValueError(ValueError):
    """:ERROR 0377:.

    Invalid HTTPD status code value '{!s:s}'.

    """

    def __init__(self, value):
        self._status = 377
        self.parameter = error(self._status) + (error(self._status)).format(value)

    def __str__(self):
        return repr(self.parameter)

    def get_status(self):
        return self._status

    status = property(get_status, None)

# ---------------------------------------------------------------------------


class sppasHTTPDStatus(object):
    """A status code value of an HTTPD server.

    HTTPD status codes are issued by a server in response to a client's
    request made to the server. All HTTP response status codes are
    separated into five classes or categories. The first digit of the
    status code defines the class of response, while the last two digits
    do not have any classifying or categorization role. There are five
    classes defined by the standard:

        - 1xx informational response – the request was received, continuing process
        - 2xx successful – the request was successfully received, understood, and accepted
        - 3xx redirection – further action needs to be taken in order to complete the request
        - 4xx client error – the request contains bad syntax or cannot be fulfilled
        - 5xx server error – the server failed to fulfil an apparently valid request

    """

    # The full list of standard status codes.
    # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
    HTTPD_STATUS = {
        100: "Continue",
        101: "Switching Protocols",
        # 102: "Processing", not standard!
        103: "Early Hints",
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        207: "Multi-Status",
        208: "Already Reported",
        226: "IM Used",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        306: "Switch Proxy",
        307: "Temporary Redirect",
        308: "Permanent Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Payload Too Large",
        414: "URI Too Long",
        415: "Unsupported Media Type",
        416: "Range Not Satisfiable",
        417: "Expectation Failed",
        418: "I'm a teapot",        # My favorite: https://en.wikipedia.org/wiki/HTTP_418
        421: "Misdirected Request",
        422: "Unprocessable Entity",
        423: "Locked",
        424: "Failed Dependency",
        425: "Too Early",
        426: "Upgrade Required",
        428: "Precondition Required",
        429: "Too Many Requests",
        431: "Request Header Fields Too Large",
        451: "Unavailable For Legal Reasons",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
        506: "Variant Also Negotiates",
        507: "Insufficient Storage",
        508: "Loop Detected",
        510: "Not Extended",
        511: "Network Authentication Required"
    }

    # -----------------------------------------------------------------------

    @staticmethod
    def check(value):
        """Raise an exception if given status value is invalid.

        :param value: (int) A response status.
        :raises: sppasHTTPDValueError
        :return: (int) value

        """
        try:
            value = int(value)
        except ValueError:
            raise sppasHTTPDValueError(value)

        if value not in sppasHTTPDStatus.HTTPD_STATUS.keys():
            raise sppasHTTPDValueError(value)

        return value

    # -----------------------------------------------------------------------

    def __init__(self):
        """Create the private member for the status code.

        Default status code is 200 for an "OK" httpd response.

        """
        self.__scode = 200

    # -----------------------------------------------------------------------

    def get(self):
        """Return the status code value (int)."""
        return self.__scode

    def set(self, value):
        """Set a new value to the status code.

        :param value: (int) HTTPD status code value.
        :raises: sppasHTTPDValueError

        """
        value = self.check(value)
        self.__scode = value

    code = property(get, set)

    # -----------------------------------------------------------------------
    # Overloads
    # -----------------------------------------------------------------------

    def __str__(self):
        return str(self.__scode)

    # -----------------------------------------------------------------------

    def __repr__(self):
        return "{:d}: {:s}".format(self.__scode, sppasHTTPDStatus.HTTPD_STATUS[self.__scode])

    # -----------------------------------------------------------------------

    def __eq__(self, other):
        return self.__scode == other
