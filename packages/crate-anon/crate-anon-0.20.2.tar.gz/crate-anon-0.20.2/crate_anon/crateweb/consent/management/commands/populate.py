#!/usr/bin/env python

"""
crate_anon/crateweb/consent/management/commands/populate.py

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

**Django management command to populate the database with leaflet entries.**

"""

from typing import Any

from django.core.management.base import BaseCommand

from crate_anon.crateweb.consent.models import Leaflet


class Command(BaseCommand):
    """
    Django management command to populate the database with leaflet entries.
    """

    help = "Populate the database with leaflet entries if necessary"

    def handle(self, *args: str, **options: Any) -> None:
        # docstring in superclass
        Leaflet.populate()
        self.stdout.write("Successfully populated leaflets")
