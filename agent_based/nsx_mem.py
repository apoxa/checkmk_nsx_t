#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict

from .agent_based_api.v1 import register
from .agent_based_api.v1.type_defs import StringTable

Section = Dict[str, int]


def parse_nsx_mem(string_table: StringTable) -> Section:
    mem_info: Section = {}

    for line in string_table:
        mem_info[line[0]] = int(line[1]) * 1024

    return mem_info


register.agent_section(
    name="nsx_mem",
    parse_function=parse_nsx_mem,
    parsed_section_name="mem_used",
)
