# Library Imports
from dataclasses import dataclass
from typing import Optional

# Local Imports
from .meraki_model import MerakiModel


@dataclass
class Device(MerakiModel):
    serial: str
    network_id: str
    name: str

    address: str
    configuration_updated_at: str
    details: list[dict[str, str]]
    firmware: str
    lan_ip: str
    lat: float
    lng: float
    mac: str
    model: str
    notes: str
    product_type: str
    tags: list[str]
    url: str

    __required_fields__ = {"serial", "network_id"}