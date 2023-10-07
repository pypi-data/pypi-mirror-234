#!/usr/bin/env python

"""
crate_anon/crateweb/userprofile/migrations/0007_auto_20170507_1218.py

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

**Userprofile app, migration 0007.**

"""
# Generated by Django 1.10.5 on 2017-05-07 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userprofile", "0006_auto_20170212_0137"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="is_clinician",
            field=models.BooleanField(
                default=False,
                verbose_name=(
                    "User is a clinician (with implied permission to look up"
                    " RIDs)"
                ),
            ),  # noqa
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="is_consultant",
            field=models.BooleanField(
                default=False,
                verbose_name=(
                    "User is an NHS consultant (relevant for clinical trials)"
                ),
            ),  # noqa
        ),
    ]
