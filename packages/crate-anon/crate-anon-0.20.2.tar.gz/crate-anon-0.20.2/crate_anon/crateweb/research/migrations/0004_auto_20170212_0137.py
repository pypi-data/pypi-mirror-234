#!/usr/bin/env python

"""
crate_anon/crateweb/research/migrations/0004_auto_20170212_0137.py

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

**Research app, migration 0004.**

"""
# Generated by Django 1.10.5 on 2017-02-12 01:37
from __future__ import unicode_literals

from cardinal_pythonlib.django.fields.jsonclassfield import JsonClassField
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("research", "0003_patientexplorer_patientexploreraudit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patientexplorer",
            name="patient_multiquery",
            field=JsonClassField(
                null=True, verbose_name="PatientMultiQuery as JSON"
            ),  # noqa
        ),
        migrations.AlterField(
            model_name="query",
            name="args",
            field=JsonClassField(
                null=True, verbose_name="SQL arguments (as JSON)"
            ),  # noqa
        ),
    ]
