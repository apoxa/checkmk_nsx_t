#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Union, List

from .agent_based_api.v1 import register
from .agent_based_api.v1.type_defs import StringTable

Section = Dict[str, Union[float, List[float], int]]


def parse_nsx_cpu(string_table: StringTable) -> Section:
    cpu_info: Section = {
        "num_cpus": int(string_table[0][0]),
        "load": [float(i) for i in string_table[1]],
        "num_threads": 0,  # this is actually wrong, but I don't know how to exclude the cpu_threads check
    }

    return cpu_info


register.agent_section(
    name="nsx_cpu",
    parse_function=parse_nsx_cpu,
    parsed_section_name="cpu",
)
