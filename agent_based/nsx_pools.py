#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import (
    Dict,
    Mapping,
    Optional,
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
    "PARTIALLY_UP": State.WARN,
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


def cluster_check_nsx_pools(item: str, section: Mapping[str, Optional[Section]]) -> CheckResult:
    yield Result(state=State.OK, summary='Nodes: %s' % ', '.join(section.keys()))
    for node_section in section.values():
        if item in node_section:
            yield from check_nsx_pools(item, node_section)
            return


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
