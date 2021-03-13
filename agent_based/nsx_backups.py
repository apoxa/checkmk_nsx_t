#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any, TypedDict, Mapping
from datetime import datetime

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    check_levels,
    render,
)

from .agent_based_api.v1.type_defs import (
    StringTable,
    CheckResult,
    DiscoveryResult,
)


class BackupData(TypedDict, total=False):
    nodeid: str
    starttime: datetime
    endtime: datetime
    success: str


Section = Mapping[str, BackupData]

Items = {
    "cluster_backup_statuses": "Cluster",
    "inventory_backup_statuses": "Inventory",
    "node_backup_statuses": "Nodes",
}


def parse_nsx_backups(string_table: StringTable) -> Section:
    parsed: Section = {}
    for item in Items.keys():
        parsed.setdefault(Items[item], {})

    for line in string_table:
        backuptype = Items.get(line[0], "UNKNOWN")
        result = BackupData()
        result["nodeid"] = line[1]
        result["starttime"] = datetime.fromtimestamp(int(line[2]) / 1000)
        result["endtime"] = datetime.fromtimestamp(int(line[3]) / 1000)
        result["success"] = line[4]
        parsed[backuptype] = result

    return parsed


register.agent_section(
    name="nsx_backups",
    parse_function=parse_nsx_backups,
)


def discover_nsx_backups(section: Section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)


def check_nsx_backups(
    item: str,
    params: Mapping[str, Any],
    section: Section,
) -> CheckResult:
    if item not in section:
        return

    age_levels_upper = params.get("age_levels_upper")

    backup = section.get(item)
    if not backup:
        yield (
            Result(state=State.CRIT, summary="No Backup found")
            if age_levels_upper
            else Result(state=State.OK, summary="No Backup found and none needed")
        )
        return

    if backup["success"] != "True":
        yield Result(state=State.CRIT, summary="Last Backup failed!")

    now = datetime.now()
    last_backup = backup.get("starttime")
    if last_backup:
        yield from check_levels(
            value=(now - last_backup).total_seconds(),
            levels_upper=age_levels_upper,
            metric_name="age",
            render_func=render.timespan,
            label="Age",
            boundaries=(0, None),
        )

    yield Result(state=State.OK, summary=f"Time: {backup.get('starttime')}")


def cluster_check_nsx_backups(
    item: str,
    params: Mapping[str, Any],
    section: Mapping[str, Section],
) -> CheckResult:
    yield Result(state=State.OK, summary='Nodes: %s' % ', '.join(section.keys()))
    for node_section in section.values():
        if item in node_section:
            yield from check_nsx_backups(item, node_section)
            return


register.check_plugin(
    name="nsx_backups",
    service_name="NSX Backups %s",
    discovery_function=discover_nsx_backups,
    check_function=check_nsx_backups,
    cluster_check_function=cluster_check_nsx_backups,
    check_ruleset_name="nsx_backups_status",
    check_default_parameters={
        "age_levels_upper": (
            60 * 60 * 26,
            60 * 60 * 50,
        )
    },
)
