# -*- coding: UTF-8 -*-
"""
:filename: response.py
:author: Brigitte Bigi
:contributor: Florian Lopitaux
:contact: develop@sppas.org
:summary: An example of custom response with HTML, JS and JSON.

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

import random
import logging
import time

from whakerpy.htmlmaker import HTMLNode
from whakerpy.htmlmaker import HTMLButtonNode
from whakerpy.httpd import sppasHTTPDStatus
from whakerpy.httpd.hresponse import BaseResponseRecipe

# ---------------------------------------------------------------------------

# javascript code example to send a post request and get data in response
JS_VALUE = """
const requestManager = new RequestManager();

async function setRandomColor() {
    // test with text post request
    // const response = await requestManager.send_post_request("update_text_color=true");

    // test with json post request
    const response = await requestManager.send_post_request({update_text_color: true}, true);

    let date = new Date();
    console.log("time to receive server response: " + (date.getTime() - response["time"]) + "ms");

    let h2Element = document.getElementsByTagName("h2")[0];
    h2Element.style.color = response["random_color"];
}

// we use a timeout to allow time for the page to load
window.onload = setTimeout(() => {
    // loop every 1.5s times
    setInterval(() => {
        setRandomColor();
    }, 1500);
}, 2000);

"""

# ---------------------------------------------------------------------------


class TestsResponseRecipe(BaseResponseRecipe):

    def __init__(self):
        super(TestsResponseRecipe, self).__init__(name="WhakerPy Test")

        # Define this HTMLTree identifier
        self._htree.add_html_attribute("id", "whakerpy")

        # Create the dynamic response content. That's why we are here!
        self._status = sppasHTTPDStatus()
        self._bake()

    # -----------------------------------------------------------------------

    @staticmethod
    def page() -> str:
        """Return the HTML page name."""
        return "whakerpy.html"

    # -----------------------------------------------------------------------

    def create(self):
        """Override. Create the fixed HTML page content.

        The fixed content corresponds to the parts that are not invalidated:
        head, body_header, body_footer, body_script.

        It can be created with htmlmaker, node by node, or loaded from a file.

        """
        # Define this page title
        self._htree.head.title(self._name)

        # Add elements in the header
        _h1 = HTMLNode(self._htree.body_header.identifier, None, "h1", value="Test of WhakerPy")
        self._htree.body_header.append_child(_h1)

        _p = HTMLNode(self._htree.body_header.identifier, None, "p",
                      value="The text is changing color without refreshing the page!")
        self._htree.body_header.append_child(_p)

        # Add an element in the footer
        _p = HTMLNode(self._htree.body_footer.identifier, None, "p",
                       value="Copyleft 2023 WhakerPy")
        self._htree.body_footer.append_child(_p)

        # The javascript
        self._htree.body_script.set_value(JS_VALUE)

    # -----------------------------------------------------------------------

    def _process_events(self, events) -> bool:
        """Process the given events coming from the POST of any form.

        :param events (dict): key=event_name, value=event_value
        :return: (bool) True if the whole page must be re-created.

        """
        logging.debug(" >>>>> Page WhakerPy -- Process events: {} <<<<<< ".format(events))
        self._status.code = 200
        dirty = False

        for event_name in events.keys():
            if event_name == "update_text_color":
                random_color = self.__generate_random_color()
                self._data = {"random_color": random_color, "time": round(time.time() * 1000)}

            elif event_name == "update_btn_text_event":
                dirty = True

            else:
                logging.warning("Ignore event: {:s}".format(event_name))

        return dirty

    # -----------------------------------------------------------------------

    def _invalidate(self):
        """Remove all children nodes of the body "main".

        Delete the body main content and nothing else.

        """
        node = self._htree.body_main
        for i in reversed(range(node.children_size())):
            node.pop_child(i)

    # -----------------------------------------------------------------------

    def _bake(self):
        """Create the dynamic page content in HTML.

        (re-)Define dynamic content of the page (nodes that are invalidated).

        """
        self.comment("Body content")
        text = TestsResponseRecipe.__generate_random_text()
        logging.debug(" -> new dynamic content: {:s}".format(text))

        # The easiest way to create an element and add it into the body->main
        h2 = self.element("h2")
        h2.set_value("Rainbow HTTP response {:d}".format(self._status.code))

        # The powered way to do the same!
        p = HTMLNode(self._htree.body_main.identifier, None, "p",
                     value="Click the button to re-create the dynamic content of the page.")
        self._htree.body_main.append_child(p)

        attr = dict()
        attr["onkeydown"] = "notify_event(this);"
        attr["onclick"] = "notify_event(this);"
        b = HTMLButtonNode(self._htree.body_main.identifier, "update_btn_text", attributes=attr)
        b.set_value(text)
        self._htree.body_main.append_child(b)

    # ------------------------------------------------------------------
    # Our back-end application.... can random things.
    # ------------------------------------------------------------------

    @staticmethod
    def __generate_random_color() -> str:
        """Returns a random color.

        Example to the request system.

        :return: (str) The random color

        """
        colors = ["red", "green", "yellow", "blue", "black", "pink", "orange", "maroon", "aqua", "silver", "purple"]
        random_index_color = random.randrange(len(colors))

        return colors[random_index_color]

    # ------------------------------------------------------------------

    @staticmethod
    def __generate_random_text() -> str:
        """Returns a random text.

        :return: (str) The random text

        """
        pronoun = ["I", "you", "we"]
        verb = ["like", "see", "paint"]
        colors = ["red", "green", "yellow", "blue", "black", "pink", "orange", "maroon", "aqua", "silver", "purple"]

        return pronoun[random.randrange(len(pronoun))] + " " \
            + verb[random.randrange(len(verb))] + " " \
            + colors[random.randrange(len(colors))]
