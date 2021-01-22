#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Union, List, Mapping, Any

from .agent_based_api.v1 import register, Service, State, Result
from .agent_based_api.v1.type_defs import StringTable, CheckResult, DiscoveryResult

from cmk.base.check_legacy_includes.cpu_load import check_cpu_load_generic

Section = Dict[str, Union[float, List[float]]]


def parse_nsx_cpu(string_table: StringTable) -> Section:
    cpu_info: Section = {
        "num_cpus": int(string_table[0][0]),
        "load": [float(i) for i in string_table[1]],
    }

    return cpu_info


register.agent_section(
    name="nsx_cpu",
    parse_function=parse_nsx_cpu,
)


def discover_nsx_cpu(section: Section) -> DiscoveryResult:
    if not section:
        return
    yield Service()


def check_nsx_cpu(params: Mapping[str, Any], section: Section) -> CheckResult:
    state, summary, perfdata = check_cpu_load_generic(
        {}, section["load"], section["num_cpus"]
    )
    yield Result(state=State(state), summary=summary)
    # TODO show metrics


register.check_plugin(
    name="nsx_cpu",
    service_name="CPU utilization",
    discovery_function=discover_nsx_cpu,
    check_function=check_nsx_cpu,
    check_default_parameters={},
)
