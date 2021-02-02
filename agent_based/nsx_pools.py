#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import (
    Dict,
    Mapping,
)

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
)

from .agent_based_api.v1.type_defs import (
    StringTable,
    CheckResult,
    DiscoveryResult,
)

import json

Section = Dict[str, Dict[str, str]]

_ENABLED_MAP = {
    "True": (State.OK, "enabled"),
    "False": (State.WARN, "disabled"),
}

_STATUS_MAP = {
    "UP": State.OK,
    "DOWN": State.CRIT,
    "DISABLED": State.WARN,
}


def parse_nsx_pools(string_table: StringTable) -> Section:
    parsed: Section = {}

    for pool in json.loads(string_table[0][0]) or []:
        parsed.setdefault(pool["display_name"], pool)

    return parsed


def discover_nsx_pools(section: Section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)


def check_nsx_pools(item: str, section: Section) -> CheckResult:
    if item not in section:
        return

    pool = section[item]

    yield Result(
        state=_STATUS_MAP.get(pool["status"], State.UNKNOWN),
        summary=f"State: {pool['status']}",
    )

    yield Result(state=State.OK, summary=f"ID: {pool['pool_id']}")


def cluster_check_nsx_pools(item: str, section: Mapping[str, Section]) -> CheckResult:
    datasets, nodeinfos = [], []
    for node, data in section.items():
        if item in data:
            datasets.append(data[item].copy())
            nodeinfos.append(node)

    if len(datasets) == 0:
        return

    yield Result(state=State.OK, summary="%s" % "/".join(nodeinfos))

    # In the 1.6 version of this check, a different node may have been
    # checked as in Python 2.7 dicts were unordered.
    yield from check_nsx_pools(item, {item: datasets[0]})


register.agent_section(
    name="nsx_pools",
    parse_function=parse_nsx_pools,
)

register.check_plugin(
    name="nsx_pools",
    service_name="NSX Pool %s",
    discovery_function=discover_nsx_pools,
    check_function=check_nsx_pools,
    cluster_check_function=cluster_check_nsx_pools,
)
