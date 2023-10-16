"""
:filename: sppas.ui.htmlmaker.treeelts.py
:author:   Brigitte Bigi
:contact:  develop@sppas.org
:summary: Node classes to generate HTML elements.

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

Since the early days of the World Wide Web, there have been many versions:
[source: <https://www.w3schools.com/html/html_intro.asp>]

-    1989: 	Tim Berners-Lee invented www
-    1991: 	Tim Berners-Lee invented HTML
-    1993: 	Dave Raggett drafted HTML+
-    1995: 	HTML Working Group defined HTML 2.0
-    1997: 	W3C Recommendation: HTML 3.2
-    1999: 	W3C Recommendation: HTML 4.01
-    2000: 	W3C Recommendation: XHTML 1.0
-    2008: 	WHATWG HTML5 First Public Draft
-    2012: 	WHATWG HTML5 Living Standard
-    2014: 	W3C Recommendation: HTML5
-    2016: 	W3C Candidate Recommendation: HTML 5.1
-    2017: 	W3C Recommendation: HTML5.1 2nd Edition
-    2017: 	W3C Recommendation: HTML5.2

HTML elements are generally made of a start tag, an optional element content,
and an end tag. However, several elements have only a start tag, like <br/>
or <img/>, and a few elements don't have tag at all, like comments.

"""

from .hexc import NodeChildTagError

from .emptynodes import EmptyNode
from .tagnodes import HTMLNode

# ---------------------------------------------------------------------------


class HTMLHeadNode(HTMLNode):
    """Convenient class to represent the head node of an HTML tree.

    """

    # List of accepted child tags in an HTML header.
    HEADER_TAGS = ("title", "meta", "link", "style", "script")

    # -----------------------------------------------------------------------

    def __init__(self, parent):
        """Create the head node."""
        super(HTMLHeadNode, self).__init__(parent, "head", "head")

    # -----------------------------------------------------------------------
    # Invalidate some of the Node methods.
    # -----------------------------------------------------------------------

    def append_child(self, node) -> None:
        """Append a child node.

        :param node: (Node)

        """
        if node.tag not in HTMLHeadNode.HEADER_TAGS:
            raise NodeChildTagError(node.tag)
        HTMLNode.append_child(self, node)

    # -----------------------------------------------------------------------

    def insert_child(self, pos, node) -> None:
        """Insert a child node at the given index.

        :param pos: (int) Index position
        :param node: (Node)

        """
        if node.tag not in HTMLHeadNode.HEADER_TAGS:
            raise NodeChildTagError(node.tag)
        HTMLNode.insert_child(self, pos, node)

    # -----------------------------------------------------------------------
    # Add convenient methods to manage the head
    # -----------------------------------------------------------------------

    def title(self, title) -> None:
        """Set the title to the header.

        :param title: (str) The page title (expected short!)

        """
        for child in self._children:
            if child.identifier == "title":
                child.set_value(title)
                break

    # -----------------------------------------------------------------------

    def meta(self, metadict) -> None:
        """Append a new meta tag to the header.

        :param metadict: (dict)

        """
        if isinstance(metadict, dict) is False:
            raise TypeError("Expected a dict.")

        child_node = EmptyNode(self.identifier, None, "meta", attributes=metadict)
        self._children.append(child_node)

    # -----------------------------------------------------------------------

    def link(self, rel, href, link_type=None) -> None:
        """Add a link tag to the header.

        :param rel: (str)
        :param href: (str) Path and/or name of the link reference
        :param link_type: (str) Mimetype of the link file

        """
        d = dict()
        d["rel"] = rel
        d["href"] = href
        if link_type is not None:
            d["type"] = link_type
        child_node = EmptyNode(self.identifier, None, "link", attributes=d)
        self._children.append(child_node)

    # -----------------------------------------------------------------------

    def script(self, src, script_type) -> None:
        """Add a meta tag to the header.

        :param src: (str) Script source file
        :param script_type: (str) Script type

        """
        d = dict()
        d["src"] = src
        d["type"] = script_type

        child_node = HTMLNode(self.identifier, None, "script", attributes=d)
        self._children.append(child_node)

    # -----------------------------------------------------------------------

    def css(self, script_content) -> None:
        """Append css style content.

        :param script_content: (str) CSS content

        """
        child_node = HTMLNode(self.identifier, None, "style", value=str(script_content))
        self._children.append(child_node)


class HTMLHeaderNode(HTMLNode):
    """Convenient class to represent the header node of an HTML tree.

    """
    def __init__(self, parent):
        """Create the main node.

        """
        super(HTMLHeaderNode, self).__init__(parent, "body_header", "header")


class HTMLNavNode(HTMLNode):
    """Convenient class to represent the nav node of an HTML tree.

    """
    def __init__(self, parent):
        """Create the nav node."""
        super(HTMLNavNode, self).__init__(parent, "body_nav", "nav")


class HTMLMainNode(HTMLNode):
    """Convenient class to represent the main node of an HTML tree.

    """
    def __init__(self, parent):
        """Create the main node."""
        super(HTMLMainNode, self).__init__(parent, "body_main", "main")


class HTMLFooterNode(HTMLNode):
    """Convenient class to represent the footer node of an HTML tree.

    """

    def __init__(self, parent):
        """Create the footer node."""
        super(HTMLFooterNode, self).__init__(parent, "body_footer", "footer")


class HTMLScriptNode(HTMLNode):
    """Convenient class to represent the scripts node of an HTML tree."""

    def __init__(self, parent):
        """Create the script node."""
        super(HTMLScriptNode, self).__init__(parent, "body_script", "script")