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

SECTION = Dict[str, Dict[str, str]]

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


def parse_nsx_vservers(string_table: StringTable) -> SECTION:
    parsed: SECTION = {}

    for line in string_table:
        parsed.setdefault(
            line[3],
            {
                "id": line[0],
                "status": line[1],
                "enabled": line[2],
            },
        )

    return parsed


def discover_nsx_vservers(section: SECTION) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)


def check_nsx_vservers(item: str, section: SECTION) -> CheckResult:
    if item not in section:
        return

    vserver = section[item]
    enabled_state, enabled_txt = _ENABLED_MAP.get(
        vserver["enabled"], (State.UNKNOWN, "unknown[%s]" % vserver["enabled"])
    )
    yield Result(state=enabled_state, summary=f"is {enabled_txt}")

    yield Result(
        state=_STATUS_MAP.get(vserver["status"], State.UNKNOWN),
        summary=f"State: {vserver['status']}",
    )

    yield Result(state=State.OK, summary=f"ID: {vserver['id']}")


def cluster_check_nsx_vservers(
    item: str, section: Mapping[str, Optional[SECTION]]
) -> CheckResult:
    yield Result(state=State.OK, summary="Nodes: %s" % ", ".join(section.keys()))
    for node_section in section.values():
        if item in node_section:
            yield from check_nsx_vservers(item, node_section)
            return


register.agent_section(
    name="nsx_vservers",
    parse_function=parse_nsx_vservers,
)

register.check_plugin(
    name="nsx_vservers",
    service_name="NSX Virtual Server %s",
    discovery_function=discover_nsx_vservers,
    check_function=check_nsx_vservers,
    cluster_check_function=cluster_check_nsx_vservers,
)
