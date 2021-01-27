#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Copyright (C) 2021  Benjamin Stier <b.stier@levigo.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


register_check_parameters(
    subgroup_applications,
    "backups",
    _("Time since last backup"),
    Dictionary(
        elements=[
            (
                "levels",
                Tuple(
                    title=_("Time since of last backup"),
                    elements=[
                        Integer(
                            title=_("Warning Level for time since last backup"),
                            help=_("Warning Level for time since last backup."),
                            unit=_("days"),
                            default_value=7,
                        ),
                        Integer(
                            title=_("Critical Level for time since last backup"),
                            help=_("Critical Level for time since last backup."),
                            unit=_("days"),
                            default_value=14,
                        ),
                    ],
                ),
            ),
        ],
    ),
    None,
    "dict",
)

register_check_parameters(
    subgroup_os,
    "nsx_memory",
    _("Main memory usage of VMWare NSX system"),
    Dictionary(
        elements=[
            (
                "levels",
                Tuple(
                    title=_("Specify levels in percentage of total RAM"),
                    elements=[
                        Percentage(
                            title=_("Warning at a RAM usage of"),
                            help=_("Warning level if memory usage is above"),
                            default_value=80.0,
                        ),
                        Percentage(
                            title=_("Critical at a RAM usage of"),
                            help=_("Critical level if memory usage is above"),
                            default_value=90.0,
                        ),
                    ],
                ),
            ),
        ],
    ),
    None,
    match_type="dict",
)
