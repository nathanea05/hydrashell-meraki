# Library Imports
from dataclasses import dataclass
from typing import Optional

# Local Imports
from .meraki_model import MerakiModel


@dataclass
class Vlan(MerakiModel):
    """Vlan class. Note: Meraki does not include network_id in the response, so it must be inserted manually before calling Vlan.from_dict()"""
    network_id: str

    id: str
    interfac_id: str
    name: str
    subnet: str
    appliance_ip: str
    group_policy_id: str
    template_vlan_type: str
    cidr: str
    mask: int
    dhcp_relay_server_ips: list[str]
    dhcp_handling: str
    dhcp_lease_time: str
    dhcp_boot_options_enabled: bool
    dhcp_boot_next_server: str
    dhcp_boot_file_name: str
    fixed_ip_assignments: dict[str, dict]
    reserved_ip_ranges: list[dict]
    dns_name_servers: str
    dhcp_options: list[dict]
    vpn_nat_subnet: str
    mandatory_dhcp: dict
    ipv6: dict


    __required_fields__ = {"id", "network_id"}