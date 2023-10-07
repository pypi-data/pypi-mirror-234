## -*- coding: utf-8 -*-
<%doc>

crate_anon/crateweb/specimen_archives/basic/progress_notes.mako

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

</%doc>

<%inherit file="inherit/base.mako"/>

<%block name="template_description">Progress Notes</%block>

<%

sql = """
    SELECT
        note_datetime AS 'When',
        note AS 'Note'
    FROM note
    WHERE brcid = ?
    ORDER BY note_datetime DESC
"""
args = [patient_id]
cursor = execute(sql, args)

%>

<%include file="snippets/results_table.mako" args="cursor=cursor"/>
