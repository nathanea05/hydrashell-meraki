# Library Imports
import meraki
from dataclasses import dataclass, field
from typing import Optional, ClassVar
from getpass import getpass

# Hydrashell Imports
from sdk.models import Context, Session, ParsedCommand
from sdk.exceptions import ExitHead

# Local Imports
from ..models.organization import Organization
from ..models.network import Network
from ..models.device import Device
from ..models.vlan import Vlan
from ..models.ssid import Ssid
from ..models.switchport import Switchport


@dataclass
class MerakiContext(Context):
    """Class to store and manage data related to the current instance of the Meraki Head.
    Each resource is grouped into levels. Only 1 resource from each level may be active at a time.
    
    • dashboard: Meraki dashboard api

    # Level 0: Organization
    • org: The active Meraki organization.

    # Level 1: Network
    • network: List of active networks

    # Level 2: Devices, Vlans, and SSIDs
    • switch: List of active switches\n
    • wireless: List of active wireless devices (access points)\n
    • appliance: List of active appliances (firewalls)\n
    • vlan: List of active vlans\n
    • ssid: List of active SSIDs\n

    # Level 3: Ports
    • switchport: List of active switchports

    # Others
    • dashboard: Meraki dashboard api
    • is_all_networks: Boolean representing whether or not the active networks are all networks in the active org
    """


    # Level 0
    org: Optional[Organization] = None

    # Level 1
    network: Optional[list[Network]] = None

    # Level 2
    switch: Optional[list[Device]] = None
    wireless: Optional[list[Device]] = None
    appliance: Optional[list[Device]] = None

    vlan: Optional[list[Vlan]] = None
    ssid: Optional[list[Ssid]] = None

    # Level 3
    switchport: Optional[list[Switchport]] = None

    # Others

    is_all_networks: Optional[bool] = False
    dashboard: Optional[meraki.DashboardAPI] = None


    LEVELS: ClassVar[dict[int, tuple[str, ...]]] = {
        0: ("org",),
        1: ("network", "is_all_networks"),
        2: ("switch", "wireless", "appliance", "vlan", "ssid"),
        3: ("switchport",),
    }

    # Reverse lookup: ATTRIBUTE_LEVEL[attr_name] -> int(level)
    ATTRIBUTE_LEVEL: ClassVar[dict[str, int]] = {
        attr: level
        for level, attrs in LEVELS.items()
        for attr in attrs
    }

    # Misc Helpers
    def get_network_ids(self) -> list[str]:
        network_ids = []
        if not self.network:
            return network_ids
        for net in self.network:
            network_ids.append(net.id)
        return(network_ids)


    # Manage Active Resources

    def clear_from_level(self, level: int):
        """Clears all attributes greater than or equal to the provided level"""
        valid_levels = self.LEVELS.keys()
        if level not in valid_levels:
            raise ValueError(f"Developer Error: Invalid level to clear: {level}. Must be one of: {valid_levels}")
        
        for lvl in self.LEVELS:
            if lvl >= level:
                for attr in self.LEVELS[lvl]:
                    setattr(self, attr, None)


    def activate(self, attr_name: str, value):
        """Activates the specified attribute and clears dependent resources"""
        if not hasattr(self, attr_name):
            raise ValueError(f"Attribute does not exist: {attr_name}")
        
        # Clear all values at or above the attribute level
        attr_level = self.ATTRIBUTE_LEVEL[attr_name]
        self.clear_from_level(attr_level)

        # Set the attribute
        setattr(self, attr_name, value)

    
    # Hydrashell Requirements

    def repr_attr(self, attr_name, description=None) -> str:
        """Returns a string representing the specified attribute"""
        attr = getattr(self, attr_name)
        if not attr:
            return None
        if len(attr) == 1:
            attr = attr[0]
            if hasattr(attr, "name"):
                return getattr(attr, "name")
            elif hasattr(attr, "id"):
                return getattr(attr, "id")
            else:
                return "Unknown resource"
        else:
            return f"{len(attr)} {description}"


    def get_prompt(self) -> str:

        parts = []

        # Level 0
        if self.org:
            parts.append(self.org.name)

        # Level 1
        if self.network:
            parts.append(self.repr_attr("network", "Networks"))

        # Level 2
        if self.switch:
            parts.append(self.repr_attr("switch", "Switches"))

        if self.wireless:
            parts.append(self.repr_attr("wireless", "Access Points"))

        if self.appliance:
            parts.append(self.repr_attr("appliance", "Appliances"))

        if self.vlan:
            parts.append(self.repr_attr("vlan", "VLANs"))

        if self.ssid:
            parts.append(self.repr_attr("ssid", "SSIDs"))

        # Level 3
        if self.switchport:
            parts.append(self.repr_attr("switchport", "Switchports"))

        
        return "\\".join(parts)
    

    def exit(self):
        # find deepest active level and clear it
        for level in reversed(sorted(self.LEVELS)):
            # if any field in this level is set, clear it and return
            if any(getattr(self, attr, None) for attr in self.LEVELS[level]):
                self.clear_from_level(level)
                return

        raise ExitHead

