# Library Imports
from dataclasses import dataclass
from typing import Optional

# Local Imports
from .meraki_model import MerakiModel


@dataclass
class Network(MerakiModel):
    id: str
    organization_id: str

    name: Optional[str]
    product_types: Optional[list[str]]
    time_zone: Optional[str]
    tags: Optional[list[str]]
    enrollment_string: Optional[str]
    url: Optional[str]
    notes: Optional[str]
    is_bound_to_config_template: Optional[bool]

    __required_fields__ = {"id", "name"}
