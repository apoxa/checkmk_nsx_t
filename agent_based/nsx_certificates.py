#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import (
    Any,
    Dict,
    Mapping,
    TypedDict,
    Optional,
)

from .agent_based_api.v1 import (
    check_levels,
    register,
    Service,
)

from .agent_based_api.v1.type_defs import (
    StringTable,
    CheckResult,
    DiscoveryResult,
)

from datetime import datetime
import json


class CertData(TypedDict, total=False):
    id: str
    not_after: datetime
    display_name: str
    cn: str


Section = Dict[str, CertData]


def parse_nsx_certificates(string_table: StringTable) -> Section:
    parsed: Section = {}
    for cert in json.loads(string_table[0][0]) or []:
        result = CertData()
        if "id" in cert:
            result["id"] = str(cert["id"])
        if "not_after" in cert["details"]:
            result["not_after"] = datetime.fromtimestamp(
                int(cert["details"]["not_after"]) / 1000
            )
        if "subject_cn" in cert["details"]:
            result["cn"] = str(cert["details"]["subject_cn"])
        if "display_name" in cert:
            result["display_name"] = str(cert["display_name"])

        parsed.setdefault(result["display_name"], result)

    return parsed


register.agent_section(
    name="nsx_certificates",
    parse_function=parse_nsx_certificates,
)


def discover_nsx_certificates(section: Section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)


def _check_nsx_certificates(
    item: str,
    params: Mapping[str, Any],
    section: Section,
    node_name: Optional[str] = None,
) -> CheckResult:
    if item not in section:
        return

    label = "certificate valid for "
    cert = section.get(item)

    # Calculate day difference
    now = datetime.now()
    expiry = cert.get("not_after")

    yield from check_levels(
        value=(expiry - now).days,
        levels_lower=params["age_levels"],
        label=label if node_name is None else "[%s]: %s" % (node_name, label),
    )


def check_nsx_certificates(
    item: str,
    params: Mapping[str, Any],
    section: Section,
) -> CheckResult:
    yield from _check_nsx_certificates(item, params, section)


def cluster_check_nsx_certificates(
    item: str,
    params: Mapping[str, Any],
    section: Mapping[str, Optional[Section]],
) -> CheckResult:
    for node_name, node_section in section.items():
        yield from _check_nsx_certificates(
            item,
            params,
            node_section,
            node_name=node_name,
        )


register.check_plugin(
    name="nsx_certificates",
    service_name="NSX Certificate %s",
    discovery_function=discover_nsx_certificates,
    check_ruleset_name="nsx_certificates",
    check_default_parameters={
        "age_levels": (25, 10),
    },
    check_function=check_nsx_certificates,
    cluster_check_function=cluster_check_nsx_certificates,
)
