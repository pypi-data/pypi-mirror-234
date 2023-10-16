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
"""
:filename: sppas.ui.htmlmaker.basenodes.baseelts.py
:author:   Brigitte Bigi
:contact:  develop@sppas.org
:summary: HTML elements inheriting BaseNode.

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

import uuid

from .basenode import BaseNode


# ---------------------------------------------------------------------------


class Doctype(BaseNode):
    """Represent the HTML doctype of an HTML page.

    :Example:
        >>> d = Doctype()
        >>> d.serialize()
        >>> '<!DOCTYPE html>'

    All HTML documents must start with a &lt;!DOCTYPE&gt; declaration.
    The declaration is **not** an HTML tag. It is an "information" to the
    browser about what document type to expect.

    Contrariwise to previous versions, HTML5 does not require any other
    information. So this class does not accept any attribute or value.

    """

    def __init__(self):
        """Create a doctype node with no defined parent."""
        # no parent means no invalidated
        super(Doctype, self).__init__(None, str(uuid.uuid1()))

        # In HTML 5, the doctype declaration does not need to refer to a DTD.
        self._value = "<!DOCTYPE html>"

    # -----------------------------------------------------------------------

    def serialize(self, nbs: int = 4) -> str:
        """Override. Serialize the doctype.

        :param nbs: (int) Number of spaces for the indentation. Un-used.
        :return: (str)

        """
        return self._value + "\n\n"

# ---------------------------------------------------------------------------


class HTMLComment(BaseNode):
    """Represent a comment element.

    The comment tag does not support any standard attributes.

    """

    def __init__(self, parent, content=" --- "):
        """Create a comment.

        """
        super(HTMLComment, self).__init__(parent, str(uuid.uuid1()))
        self._value = content

    # -----------------------------------------------------------------------

    def serialize(self, nbs: int = 4) -> str:
        """Serialize the comment into HTML.

        :param nbs: (int) Number of spaces for the indentation
        :return: (str)

        """
        indent = " "*nbs
        html = "\n"
        html += indent + "<!-- "
        r = (70 - len(self._value)) // 2
        if r > 0:
            html += "-"*r
        html += " " + self._value + " "
        if r > 0:
            html += "-"*r
        html += " -->\n\n"
        return html

