"""
:filename: sppas.ui.htmlmaker.basenode.py
:author:   Brigitte Bigi
:contact:  develop@sppas.org
:summary: A base class for any HTML element.

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

import re
import uuid

from whakerpy.htmlmaker.hexc import NodeInvalidIdentifierError
from whakerpy.htmlmaker.hexc import NodeKeyError

# ---------------------------------------------------------------------------


class BaseNode(object):
    """A base class for any node in an HTML tree.

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

    An HTML element without content is called an empty node. It has a
    start tag but neither a content nor an end tag. It has only attributes.

    The BaseNode() class is a base class for any of these HTML elements.
    It is intended to be overridden.

    """

    def __init__(self, parent: str = None, identifier: str = None, **kwargs):
        """Create a new base node.

        :param parent: (str) Parent identifier
        :param identifier: (str) This node identifier
        :raises: NodeInvalidIdentifierError: if 'identifier' contains invalid characters or if invalid length

        """
        # The node identifier
        if identifier is not None:
            ident = BaseNode.validate_identifier(identifier)
            self.__identifier = ident
        else:
            self.__identifier = str(uuid.uuid1())

        # Identifier of the parent node
        self._parent = None
        self.set_parent(parent)

    # -----------------------------------------------------------------------

    @staticmethod
    def validate_identifier(identifier: str) -> str:
        """Return the given identifier if it matches the requirements.

        An identifier should contain at least 1 character and no whitespace.

        :param identifier: (str) Key to be validated
        :raises: NodeInvalidIdentifierError: if it contains invalid characters
        :raises: NodeInvalidIdentifierError: if invalid length
        :return: (str)

        """
        entry = BaseNode.full_strip(identifier)
        if len(entry) != len(identifier):
            raise NodeInvalidIdentifierError(identifier)

        if len(identifier) == 0:
            raise NodeInvalidIdentifierError(identifier)

        return identifier

    # -----------------------------------------------------------------------

    @staticmethod
    def full_strip(entry):
        """Fully strip the string: multiple whitespace, tab and CR/LF.

        Remove all whitespace, tab and CR/LF inside the string.

        :return: (str) Cleaned string

        """
        e = re.sub("[\s]+", r"", entry)
        e = re.sub("[\t]+", r"", e)
        e = re.sub("[\n]+", r"", e)
        e = re.sub("[\r]+", r"", e)
        if "\ufeff" in e:
            e = re.sub("\ufeff", r"", e)
        return e

    # -----------------------------------------------------------------------

    @property
    def identifier(self) -> str:
        """Return the unique ID of the node within the scope of a tree. """
        return self.__identifier

    # -----------------------------------------------------------------------

    def is_leaf(self) -> bool:
        """Return true if node has no children."""
        return True

    # -----------------------------------------------------------------------

    def is_root(self) -> bool:
        """Return true if node has no parent, i.e. as root."""
        return self._parent is None

    # -----------------------------------------------------------------------

    def get_parent(self) -> str:
        """The parent identifier.

        :return: (str) node identifier

        """
        return self._parent

    # -----------------------------------------------------------------------

    def set_parent(self, node_id: str) -> None:
        """Set the parent identifier.

        :param node_id: (str) Identifier of the parent

        """
        if self.__identifier == node_id:
            raise NodeKeyError(self.__identifier, node_id)

        self._parent = node_id

    # -----------------------------------------------------------------------

    def has_child(self, node_id: str) -> bool:
        """Return True if the given node is a direct child.

        :param node_id: (str) Identifier of the node
        :return: (bool) True if given identifier is a direct child.

        """
        return not self.is_leaf()

    # -----------------------------------------------------------------------

    def serialize(self, nbs: int = 4) -> str:
        """To be overriden. Serialize the node into HTML.

        :param nbs: (int) Number of spaces for the indentation
        :return: (str)

        """
        return ""

    # -----------------------------------------------------------------------
    # Overloads
    # -----------------------------------------------------------------------

    def __repr__(self):
        return self.serialize()

    # -----------------------------------------------------------------------

    def __str__(self):
        return "Node ({:s})".format(self.identifier)
