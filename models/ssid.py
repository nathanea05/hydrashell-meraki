# Library Imports
from dataclasses import dataclass
from typing import Optional

# Local Imports
from .meraki_model import MerakiModel


@dataclass
class Ssid(MerakiModel):
    """Ssid class.\nNote: The meraki api does not include network_id in the response. It must be manually entered before calling Ssid.from_dict()"""
    network_id: str

    number: int
    name: str
    enabled: bool
    splash_page: str
    ssid_admin_accessible: bool
    local_auth: bool
    auth_mode: str
    encryption_mode: str
    wpa_encryption_mode: str
    radius_servers: list[dict]
    radius_accounting_servers: list[dict]
    radius_accounting_enabled: bool
    radius_enabled: bool
    radius_attribute_for_group_policies: str
    radius_failover_policy: str
    radius_load_balancing_policy: str
    ip_assignment_mode: str
    admin_splash_url: str
    splash_timeout: str
    walled_garden_enabled: bool
    walled_garden_ranges: list[str]
    min_bitrate: int
    band_selection: str
    per_client_bandwidth_limit_up: int
    per_client_bandwidth_limit_down: int
    visible: bool
    available_on_all_aps: bool
    availability_tags: list[str]
    per_ssid_bandwidth_limit_up: int
    per_ssid_bandwidth_limit_down: int
    mandatory_dhcp_enabled: bool


    __required_fields__ = {"number", "network_id"}