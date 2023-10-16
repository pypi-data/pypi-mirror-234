# -*- coding: UTF-8 -*-
"""
:filename: sppas.ui.whakerpy.httpd.handler.py
:author:   Brigitte Bigi
:contributor: Florian Lopitaux
:contact:  develop@sppas.org
:summary:  Manage an HTTPD handler for any web-based application.

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

import os
import json
import logging
import http.server

from .hstatus import sppasHTTPDStatus

# ---------------------------------------------------------------------------


class sppasHTTPDHandler(http.server.BaseHTTPRequestHandler):
    """Web-based application HTTPD handler.

    This class is instantiated by the server each time a request is received
    and then a response is created. This is an HTTPD handler for any Web-based
    application server. It parses the request and the headers, then call a
    specific method depending on the request type.

    In this handler, HTML pages are supposed to not be static. Instead,
    they are serialized from an HTMLTree instance -- so not read from disk.
    The server contains the page's bakery, the handler is then asking the
    server page's bakery to get the html content and response status.

    The parent server is supposed to have all the pages as members in a
    dictionary, i.e. it's a sppasBaseHTTPDServer. Each page has a bakery
    to create the response content. However, this handler can also be used
    with any other http.server.ThreadingHTTPServer.

    The currently supported HTTPD responses status are:

        - 200: OK
        - 205: Reset Content
        - 403: Forbidden
        - 404: Not Found
        - 410: Gone
        - 418: I'm not a teapot

    """

    def _set_headers(self, status: int) -> None:
        """Set the HTTPD response headers.

        :param status: (int) A response status.
        :raises: sppasHTTPDValueError

        """
        status = sppasHTTPDStatus.check(status)
        self.send_response(status)
        self.end_headers()

    # -----------------------------------------------------------------------

    def _static_content(self, filename: str) -> tuple:
        """Return the file content and the corresponding status.

        :param filename: (str)
        :return: tuple(bytes, sppasHTTPDStatus)

        """
        if os.path.exists(filename) is True:
            if os.path.isfile(filename) is True:
                content = open(filename, "rb").read()
                return content, sppasHTTPDStatus()
            else:
                content = bytes("<html><body>Error 403: Forbidden."
                                "The client can't have access to the requested {:s}."
                                "</body></html>".format(filename), "utf-8")
                status = sppasHTTPDStatus()
                status.code = 403
                return content, status

        # it does not exist!
        content = bytes("<html><body>Error 404: Not found."
                        "The server does not have the requested {:s}."
                        "</body></html>".format(filename), "utf-8")
        status = sppasHTTPDStatus()
        status.code = 404
        return content, status

    # -----------------------------------------------------------------------

    def _json_data(self, events: dict) -> tuple:
        """Process the events and return the data and the status.

        :param events: (dict) The dictionary that contains all events posted
        by the client request.

        :return: (tuple) First element - The content of the response (json data).
                         Second element - The status of the server.

        """
        # Test if the server is our
        if hasattr(self.server, 'page_bakery') is False:
            # Server is not the custom one for SPPAS wapp.
            return self._static_content(self.path[1:])

        # Requested page name and page bakery for all the pages created
        # dynamically -- i.e. from an HTMLTree.
        page_name = os.path.basename(self.path)
        content, status = self.server.page_bakery(page_name, events, True)

        # but the HTML page may be static
        if status == 404:
            content, status = self._static_content(self.path[1:])

        return content, status

    # -----------------------------------------------------------------------

    def _html(self, events: dict) -> tuple:
        """Process the events and return the html page content and status.

        :param events: (dict) key=event name, value=event value
        :return: tuple(bytes, sppasHTTPDStatus)

        """
        # Test if the server is our
        if hasattr(self.server, 'page_bakery') is False:
            # Server is not the custom one for SPPAS wapp.
            return self._static_content(self.path[1:])

        # Requested page name and page bakery for all the pages created
        # dynamically -- i.e. from an HTMLTree.
        page_name = os.path.basename(self.path)
        content, status = self.server.page_bakery(page_name, events)

        # but the HTML page may be static
        if status == 404:
            content, status = self._static_content(self.path[1:])

        return content, status

    # -----------------------------------------------------------------------

    def _response(self, content: bytes, status: int) -> None:
        """Make the appropriate HTTPD response.

        :param content: (bytes) The HTML response content
        :param status: (int) The HTTPD status code of the response

        """
        if status == 418:
            # 418: I'm not a teapot. Used as a response to a blocked request.
            # With no response content, the browser will display an empty page.
            self._set_headers(418)
        elif status == 205:
            # 205 Reset Content. The request has been received. Tells the
            # user agent to reset the document which sent this request.
            # With no response content, the browser will continue to display
            # the current page.
            self._set_headers(205)
        else:
            self._set_headers(status)
            self.wfile.write(content)
            if status == 410:
                # 410 Gone. Only possible in the context of a local app.
                # On web, the server does not shut down when the client
                # is asking for!
                self.server.shutdown()

    # -----------------------------------------------------------------------
    # Override BaseHTTPRequestHandler classes.
    # -----------------------------------------------------------------------

    def do_HEAD(self) -> None:
        """Prepare the response to a HEAD request."""
        logging.debug("HEAD -- requested: {}".format(self.path))
        self._set_headers(200)

    # -----------------------------------------------------------------------

    def do_GET(self) -> None:
        """Prepare the response to a GET request.

        """
        logging.debug("GET -- requested: {}".format(self.path))
        if self.path == '/':
            try:
                self.path += self.server.default()
            except AttributeError:
                # Server is not the custom one for dynamic app.
                self.path += "index.html"

        if "?" in self.path:
            self.path = self.path[:self.path.index("?")]

        # The client requested an HTML page. Response content is created
        # by the server.
        if self.path.endswith("html") is True:
            content, status = self._html(dict())
        else:
            # The client requested a css, a script, an image, a font, etc.
            # These are statics' content. The handler is reading it from disk,
            # and it makes the response itself.
            content, status = self._static_content(self.path[1:])

        self._response(content, status.code)

    # -----------------------------------------------------------------------

    def do_POST(self) -> None:
        """Prepare the response to a POST request.

        """
        logging.debug("POST -- requested: {}".format(self.path))
        if self.path == '/':  # should not happen.
            try:
                self.path += self.server.default()
            except AttributeError:
                # Server is not the custom one.
                self.path += "index.html"

        events = dict()

        # Extract the posted data of the request.
        content_len = int(self.headers.get('Content-Length'))
        data = self.rfile.read(content_len).decode("utf-8")

        # Convert data if it's in JSON format
        if "application/json" in self.headers.get('Content-Type'):
            try:
                events = json.loads(data)
            except json.JSONDecodeError:
                logging.error("Can't decode JSON POSTED data : {}".format(data))

        # Convert data if it's in text format
        else:
            # Parse the posted data of the request. It should be of the form:
            # name_of_something=its_value&name2=value2&name3=value3
            logging.debug("POST -- data: {}".format(data))
            for dinput in data.split("&"):
                new_event = dinput.split("=")
                if len(new_event) == 2:
                    events[new_event[0]] = new_event[1]
                else:
                    logging.error("Can't understand POSTED data: {}".format(dinput))

        # Create the response
        if "application/json" in self.headers.get('Accept'):
            content, status = self._json_data(events)
        else:
            content, status = self._html(events)

        self._response(content, status.code)

    # -----------------------------------------------------------------------

    def log_request(self, code='-', size='-') -> None:
        """Override. For a quiet handler pls!!!."""
        pass
