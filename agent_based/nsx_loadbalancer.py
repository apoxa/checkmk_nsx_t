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

SECTION = Dict[str, Dict[str, str]]

_ENABLED_MAP = {
    "True": (State.OK, "enabled"),
    "False": (State.CRIT, "disabled"),
}

_STATUS_MAP = {
    "UP": State.OK,
    "DISABLED": State.CRIT,
}


def parse_nsx_loadbalancer(string_table: StringTable) -> SECTION:
    parsed: SECTION = {}

    for line in string_table:
        instance = parsed.setdefault(
            line[0],
            {
                "id": line[1],
                "status": line[2],
                "enabled": line[3],
            },
        )
        for key, index in [
            ("l4_current_sessions", 4),
            ("l4_max_sessions", 5),
            ("l4_total_sessions", 6),
            ("l4_current_session_rate", 7),
            ("l7_current_sessions", 8),
            ("l7_max_sessions", 9),
            ("l7_total_sessions", 10),
            ("l7_current_session_rate", 11),
        ]:
            try:
                value = int(line[index])
            except (IndexError, ValueError):
                continue
            instance.setdefault(key, value)

    return parsed


register.agent_section(
    name="nsx_loadbalancer",
    parse_function=parse_nsx_loadbalancer,
)


def discover_nsx_loadbalancer(section: SECTION) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)


def check_nsx_loadbalancer(item: str, section: SECTION) -> CheckResult:
    if item not in section:
        return

    loadbalancer = section[item]
    enabled_state, enabled_txt = _ENABLED_MAP.get(
        loadbalancer["enabled"],
        (State.UNKNOWN, "unknown[%s]" % loadbalancer["enabled"]),
    )
    yield Result(state=enabled_state, summary=f"is {enabled_txt}")

    yield Result(
        state=_STATUS_MAP.get(loadbalancer["status"], State.UNKNOWN),
        summary=f"State: {loadbalancer['status']}",
    )

    yield Result(state=State.OK, summary=f"ID: {loadbalancer['id']}")

    # TODO perfdata


def cluster_check_nsx_loadbalancer(
    item: str, section: Mapping[str, SECTION]
) -> CheckResult:
    yield Result(state=State.OK, summary='Nodes: %s' % ', '.join(section.keys()))
    for node_section in section.values():
        if item in node_section:
            yield from check_nsx_loadbalancer(item, node_section)
            return


register.check_plugin(
    name="nsx_loadbalancer",
    service_name="NSX LoadBalancer %s",
    discovery_function=discover_nsx_loadbalancer,
    check_function=check_nsx_loadbalancer,
    cluster_check_function=cluster_check_nsx_loadbalancer,
)
