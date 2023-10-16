"""
:filename: sppas.ui.whakerpy.httpd.hresponse.py
:author:   Brigitte Bigi
:contact:  develop@sppas.org
:summary:  Base class to create an HTML response.

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

import os
import json

from whakerpy.htmlmaker import HTMLComment
from whakerpy.htmlmaker import HTMLNode
from whakerpy.htmlmaker import HTMLTree

from .hstatus import sppasHTTPDStatus

# ---------------------------------------------------------------------------


JS_NOTIFY_EVENT = """
function notify_event(action_btn) {
    const form = document.createElement("form");
    form.method = "POST";
    form.style.display = "none";

    const el = document.createElement("input");
    el.name = action_btn.name + "_event";
    el.id = action_btn.name + "_event";
    el.value = action_btn.getAttribute("value")
    el.type = "hidden"
    form.appendChild(el);

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}

"""

# ---------------------------------------------------------------------------


class BaseResponseRecipe(object):
    """Base class to create an HTML response file.

    """

    @staticmethod
    def page() -> str:
        """Return the HTML page name. To be overridden."""
        return "undefined.html"

    # -----------------------------------------------------------------------

    def __init__(self, name="Undefined", tree=None):
        """Create a new ResponseRecipe instance with a default response.

        """
        # Define members with default values
        self._name = name
        self._status = sppasHTTPDStatus()
        # Data to communicate with client (javascript side)
        self._data = dict()

        # Define workers: the HTML bakery
        if tree is not None and isinstance(tree, HTMLTree):
            self._htree = tree
        else:
            self._htree = HTMLTree(self._name.replace(" ", "_"))

        # Test if this tree can manage events (from buttons, forms, etc)
        shead = self._htree.head.serialize()
        if "notify_event" not in shead:
            js = HTMLNode(self._htree.head.identifier, None, "script",
                          value=JS_NOTIFY_EVENT)
            self._htree.head.append_child(js)
        if "request.js" not in shead:
            self._htree.head.script(src=os.path.join("whakerpy", "request.js"), script_type="text/javascript")

        self.create()

    # -----------------------------------------------------------------------

    def get_json_data(self) -> str:
        """Gets the current data to send to the client following this request.

        :return: (str) The json data in the string format

        """
        return json.dumps(self._data)

    # -----------------------------------------------------------------------
    # Getters
    # -----------------------------------------------------------------------

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> sppasHTTPDStatus:
        return self._status

    # -----------------------------------------------------------------------
    # Convenient methods to add HTML nodes in the body part of the tree
    # -----------------------------------------------------------------------

    def comment(self, content: str) -> HTMLComment:
        """Add a comment to the body->main.

        :param content: (str) The comment content
        :return: (HTMLComment) the created node

        """
        return self._htree.comment(content)

    # -----------------------------------------------------------------------

    def element(self, tag: str = "div", ident=None, class_name=None) -> HTMLNode:
        """Add an element node to the body->main.

        :param tag: (str) HTML element name
        :param ident: (str) Identifier of the element
        :param class_name: (str) Value of the class attribute
        :return: (HTMLNode) The created node

        """
        return self._htree.element(tag, ident, class_name)

    # -----------------------------------------------------------------------
    # Workers
    # -----------------------------------------------------------------------

    def create(self) -> None:
        """Create the fixed page content in HTML. Intended to be overridden.

        This method is intended to be used to create the parts of the tree
        that won't be invalidated when baking.

        """
        pass

    # -----------------------------------------------------------------------

    def bake(self, events) -> str:
        """Return the HTML response after processing the events.

        Processing the events may change the response status. This method is
        invoked by the HTTPD server to construct the response. Given events
        are the information the handler received (commonly with POST).

        :param events: (dict) The requested events to be processed

        """
        # Process the given events with the application
        dirty = False
        if len(events) > 0:
            dirty = self._process_events(events)

        # Re-create the page content only if something changed during
        # processing the events.
        if dirty is True:
            self._invalidate()
            self._bake()

        # Turn the page content into an HTML string.
        return self._htree.serialize()

    # -----------------------------------------------------------------------
    # Private: methods to be overridden by children to customize the recipe.
    # -----------------------------------------------------------------------

    def _process_events(self, events) -> bool:
        """Process the given events.

        The given event name must match a function of the event's manager.
        Processing an event may change the content of the tree. In that case,
        the `dirty` method must be turned into True: it will invalidate the
        deprecated content (_invalidate) and re-generate a new one (_bake).

        :param events (dict): key=event_name, value=event_value
        :return: None

        """
        self._status.code = 200
        return False

    # -----------------------------------------------------------------------

    def _invalidate(self):
        """Remove children nodes of the tree. Intended to be overridden.

        Remove the dynamic content of the tree, which will be re-introduced
        when baking.

        If the tree has no dynamic content, this method is un-used.

        """
        pass

    # -----------------------------------------------------------------------

    def _bake(self) -> None:
        """Fill in the HTML page generator. Intended to be overridden.

        If the tree has no dynamic content, this method is un-used.

        This method is baking the "dynamic" content of the page, i.e. it
        should not change the content created by the method create().

        """
        pass
