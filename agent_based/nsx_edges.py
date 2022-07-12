#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import (
    Dict,
    Mapping,
    Optional,
    TypedDict,
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


class EdgeData(TypedDict, total=False):
    id: str
    status: str
    display_name: str


Section = Dict[str, EdgeData]

_STATUS_MAP = {
    "UP": State.OK,
    "DOWN": State.CRIT,
}


def parse_nsx_edges(string_table: StringTable) -> Section:
    parsed: Section = {}
    for edge in json.loads(string_table[0][0]) or []:
        result = EdgeData()
        if "node_uuid" in edge:
            result["id"] = str(edge["node_uuid"])
        if "status" in edge:
            result["status"] = str(edge["status"])
        if "node_display_name" in edge:
            result["display_name"] = str(edge["node_display_name"])

        if "display_name" not in result:
            continue

        parsed.setdefault(result["display_name"], result)

    return parsed


register.agent_section(
    name="nsx_edges",
    parse_function=parse_nsx_edges,
)


def discover_nsx_edges(section: Section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)


def check_nsx_edges(item: str, section: Section) -> CheckResult:
    if item not in section:
        return

    edge = section[item]
    edge_state = _STATUS_MAP.get(
        edge["status"], (3, "unknown[%s]" % edge["status"]))
    yield Result(state=edge_state, summary=f"is {edge['status']}")

    yield Result(state=State.OK, summary=f"ID: {edge['id']}")


def cluster_check_nsx_edges(item: str, section: Mapping[str, Optional[Section]]) -> CheckResult:
    yield Result(state=State.OK, summary="Nodes: %s" % ", ".join(section.keys()))
    for node_section in section.values():
        if item in node_section:
            yield from check_nsx_edges(item, node_section)
            return


register.check_plugin(
    name="nsx_edges",
    service_name="NSX Edge %s",
    discovery_function=discover_nsx_edges,
    check_function=check_nsx_edges,
    cluster_check_function=cluster_check_nsx_edges,
)
