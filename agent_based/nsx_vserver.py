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
        vserver["enabled"], (3, "unknown[%s]" % vserver["enabled"])
    )
    yield Result(state=enabled_state, summary=f"is {enabled_txt}")

    yield Result(
        state=_STATUS_MAP.get(vserver["status"], 3),
        summary=f"State: {vserver['status']}",
    )

    yield Result(state=State.OK, summary=f"ID: {vserver['id']}")


def cluster_check_nsx_vservers(
    item: str, section: Mapping[str, SECTION]
) -> CheckResult:
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
    yield from check_nsx_vservers(item, {item: datasets[0]})

    # In cluster mode we check if data sets are equal from all nodes
    # else we have only one data set
    if len(
        set([y for x in list(map(lambda x: list(x.values()), datasets)) for y in x])
    ) > len(set(list(datasets[0].values()))):
        yield Result(
            state=State.UNKNOWN,
            summary="Cluster: data from nodes are not equal",
        )


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
