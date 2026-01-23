# Library Imports
from dataclasses import dataclass
from typing import Optional

# Local Imports
from .meraki_model import MerakiModel


@dataclass
class Switchport(MerakiModel):
    """Switchport class.\nNote: The meraki api does not include serial_number in the response. It must be manually entered before calling Switchport.from_dict()"""
    serial: str

    port_id: str
    name: str
    tags: list[str]
    enabled: bool
    poe_enabled: bool
    type: str
    vlan: int
    voice_vlan: int
    allowed_vlans: str
    isolation_enabled: bool
    rstp_enabled: bool
    stp_guard: str
    stp_port_fast_trunk: bool
    link_negotiation: str
    link_negotiation_capabilities: list[str]
    port_schedule_id: str
    schedule: dict
    udld: str
    access_policy_type: str
    access_policy_number: int
    mac_allow_list: list[str]
    mac_whitelist_limit: int
    sticky_mac_allow_list: list[str]
    sticky_mac_allow_list_limit: int
    storm_control_enabled: bool
    adaptive_policy_group_id: str
    adaptive_policy_group: dict
    peer_sgt_capable: bool
    flexible_stacking_enabled: bool
    dai_trusted: bool
    profile: dict
    module: dict
    mirror: dict
    dot3az: dict[str, bool]
    high_speed: dict[str, bool]

    __required_fields__ = {"number", "network_id"}