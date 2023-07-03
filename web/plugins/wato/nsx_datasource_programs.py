#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.special_agents.common import RulespecGroupVMCloudContainer
from cmk.gui.plugins.wato import (
    HostRulespec,
    IndividualOrStoredPassword,
    rulespec_registry,
)
from cmk.gui.valuespec import (
    Dictionary,
    DropdownChoice,
    TextAscii,
)
from cmk.gui.watolib.rulespecs import Rulespec


def _factory_default_special_agents_nsx():
    # No default, do not use setting if no rule matches
    return Rulespec.FACTORY_DEFAULT_UNUSED


def _valuespec_special_agents_nsx():
    return Dictionary(
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
                    default_value=False,
                ),
            ),
        ],
        optional_keys=["cert"],
    )


rulespec_registry.register(
    HostRulespec(
        factory_default=_factory_default_special_agents_nsx(),
        group=RulespecGroupVMCloudContainer,
        name="special_agents:nsx",
        valuespec=_valuespec_special_agents_nsx,
    )
)
