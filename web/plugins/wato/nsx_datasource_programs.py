#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import cmk.gui.watolib as watolib
from cmk.gui.plugins.wato import (
    IndividualOrStoredPassword,
    rulespec_registry,
    HostRulespec,
)
from cmk.gui.plugins.wato.datasource_programs import RulespecGroupDatasourcePrograms
from cmk.gui.valuespec import Dictionary, DropdownChoice, TextAscii, Transform
from cmk.gui.i18n import _


def _factory_default_special_agents_nsx():
    # No default, do not use setting if no rule matches
    return watolib.Rulespec.FACTORY_DEFAULT_UNUSED


def _transform_agent_nsx(params):
    params.setdefault("cert", False)

    return params


def _valuespec_special_agents_nsx():
    return Transform(
        Dictionary(
            title=_("Check state of a NSX-T 3.x environment"),
            help=_(
                "This rule selects the VMWare NSX-T agent instead of the normal Check_MK Agent2 and allows"
                "monitoring of NSX-T environment via NSX-T Manager API. You can configure your connection "
                "settings here."
            ),
            elements=[
                (
                    "user",
                    TextAscii(
                        title=_("Username"),
                        allow_empty=False,
                    ),
                ),
                (
                    "password",
                    IndividualOrStoredPassword(
                        title=_("Password"),
                        allow_empty=False,
                    ),
                ),
                (
                    "cert",
                    DropdownChoice(
                        title=_("SSL certificate checking"),
                        choices=[
                            (True, _("Activate")),
                            (False, _("Deactivated")),
                        ],
                    ),
                ),
            ],
            optional_keys=["cert"],
        ),
        forth=_transform_agent_nsx,
    )


rulespec_registry.register(
    HostRulespec(
        factory_default=_factory_default_special_agents_nsx(),
        group=RulespecGroupDatasourcePrograms,
        name="special_agents:nsx",
        valuespec=_valuespec_special_agents_nsx,
    )
)
