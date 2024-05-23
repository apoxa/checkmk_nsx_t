#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional

from cmk.plugins.lib.cpu import Load, Section

from .agent_based_api.v1 import register
from .agent_based_api.v1.type_defs import StringTable


def parse_nsx_cpu(string_table: StringTable) -> Optional[Section]:
    return (
        Section(
            load=Load(*(float(i) for i in string_table[1])),
            num_cpus=int(string_table[0][0]) if len(
                string_table[0]) >= 1 else 1,
        )
        if string_table
        else None
    )


register.agent_section(
    name="nsx_cpu",
    parsed_section_name="cpu",
    parse_function=parse_nsx_cpu,
)
