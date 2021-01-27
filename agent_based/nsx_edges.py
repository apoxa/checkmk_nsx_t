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

_STATUS_MAP = {
    "UP": State.OK,
    "DOWN": State.CRIT,
}


def parse_nsx_edges(string_table: StringTable) -> SECTION:
    parsed: SECTION = {}

    for line in string_table:
        parsed.setdefault(
            line[0],
            {
                "id": line[1],
                "status": line[2],
            },
        )

    return parsed


register.agent_section(
    name="nsx_edges",
    parse_function=parse_nsx_edges,
)


def discover_nsx_edges(section: SECTION) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)


def check_nsx_edges(item: str, section: SECTION) -> CheckResult:
    if item not in section:
        return

    edge = section[item]
    edge_state = _STATUS_MAP.get(edge["status"], (3, "unknown[%s]" % edge["status"]))
    yield Result(state=edge_state, summary=f"is {edge['status']}")

    yield Result(state=State.OK, summary=f"ID: {edge['id']}")


def cluster_check_nsx_edges(item: str, section: Mapping[str, SECTION]) -> CheckResult:
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
    yield from check_nsx_edges(item, {item: datasets[0]})

    # In cluster mode we check if data sets are equal from all nodes
    # else we have only one data set
    if len(
        set([y for x in list(map(lambda x: list(x.values()), datasets)) for y in x])
    ) > len(set(list(datasets[0].values()))):
        yield Result(
            state=State.UNKNOWN,
            summary="Cluster: data from nodes are not equal",
        )


register.check_plugin(
    name="nsx_edges",
    service_name="NSX Edge %s",
    discovery_function=discover_nsx_edges,
    check_function=check_nsx_edges,
    cluster_check_function=cluster_check_nsx_edges,
)