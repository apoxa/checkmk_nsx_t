#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
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


register_rule("datasource_programs",
    "special_agents:nsx",
     Dictionary(
        title = _("Check state of a NSX-T 3.x environment"),
        help = _("This rule selects the VMWare NSX-T agent"),
        elements = [
            ( "user",
              TextAScii(
                  title = _("Username"),
                  allow_empty = False,
              )
            ),
            ( "password",
              TextAscii(
                  title = _("Password"),
                  allow_empty = False,
              )
            ),
            ( "cert",
              DropdownChoice(
                  title = _("SSL certificate verification"),
                  choices = [
                      (True, _("Activate")),
                      (False, _("Deactivate")),
                  ],
              )
            ),
        ],
        optional_keys = [ 'cert' ],
    ),
    factory_default = watolib.Rulespec.FACTORY_DEFAULT_UNUSED, # No default, do not use setting if no rule matches
    match = 'first')
