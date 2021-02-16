#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    TextAscii,
    Tuple,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)


def _parameter_valuespec_nsx_certificates():
    return Dictionary(
        elements=[
            (
                "age_levels",
                Tuple(
                    title=_("Remaining days of validity"),
                    elements=[
                        Integer(
                            title=_("Warning below"),
                            default_value=25,
                            minvalue=0,
                        ),
                        Integer(
                            title=_("Critical below"),
                            default_value=10,
                            minvalue=0,
                        ),
                    ],
                ),
            ),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="nsx_certificates",
        group=RulespecGroupCheckParametersApplications,
        item_spec=lambda: TextAscii(
            title=_("Name of Certificate"),
        ),
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_nsx_certificates,
        title=lambda: _("NSX SSL certificates"),
    )
)
