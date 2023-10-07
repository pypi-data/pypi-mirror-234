#!/usr/bin/env python

"""
crate_anon/common/argparse_assist.py

===============================================================================

    Copyright (C) 2015, University of Cambridge, Department of Psychiatry.
    Created by Rudolf Cardinal (rnc1001@cam.ac.uk).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <https://www.gnu.org/licenses/>.

===============================================================================

**A combination class for rich-argparse.**

"""

from rich_argparse import (
    ArgumentDefaultsRichHelpFormatter,
    RawDescriptionRichHelpFormatter,
)


class RawDescriptionArgumentDefaultsRichHelpFormatter(
    ArgumentDefaultsRichHelpFormatter, RawDescriptionRichHelpFormatter
):
    """
    Combines the features of

    - :class:`RawDescriptionRichHelpFormatter` -- don't mangle the description
    - :class:`ArgumentDefaultsRichHelpFormatter` -- print argument defaults
    """

    pass
