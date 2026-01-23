# Library Imports
import meraki
from dataclasses import dataclass
from typing import Optional
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

def dashboard_init(api_key: str) -> meraki.DashboardAPI:
    """Initializes the meraki dashboard"""
    


@dataclass
class MerakiContext(Context):

    dashboard: Optional[meraki.DashboardAPI] = None
    org: Optional[Organization] = None
    networks: Optional[list[Network]] = None
    is_all_networks: Optional[bool] = False

    switches: Optional[set[Device]] = None
    access_points: Optional[set[Device]] = None
    firewalls: Optional[set[Device]] = None
    vlans: Optional[set[Vlan]] = None
    ssids: Optional[set[Ssid]] = None

    switchports: Optional[set[Switchport]] = None


    def get_prompt(self):
        parts = []

        if self.org:
            parts.append(self.org.name)


        if self.networks:
            parts.append(self.repr_resource(self.networks, "Networks"))

        if self.switches:
            parts.append(self.repr_devices(type="switch"))

        if self.access_points:
            parts.append(self.repr_devices(type="ap"))

        if self.firewalls:
            parts.append(self.repr_devices(type="firewall"))

        if self.vlans:
            parts.append(self.repr_resource(self.vlans, "Vlans"))

        if self.ssids:
            parts.append(self.repr_resource(self.ssids, "SSIDs"))

        if self.switchports:
            parts.append(self.repr_resource(self.switchports, "Switchports"))

        
        return "\\".join(parts)

            

    def exit(self):

        if self.switchports:
            self.switchports = None
            return
        if self.switches or self.access_points or self.firewalls or self.vlans or self.ssids:
            self.clear_devices()
            self.vlans = None
            self.ssids = None
            return
        if self.networks:
            self.networks = None
            return
        if self.org:
            self.org = None
            return
        
        # Exit head if org not set
        raise ExitHead

        
    def repr_resource(self, resource: list, resource_name: str) -> str:
        if not resource:
            return None
        if len(resource) == 1:
            return resource[0].name
        else:
            return f"{len(resource)} {resource_name}"

    
    def repr_devices(self, type: str) -> str:
        d = None
        if type == "switch":
            d = self.switches
        if type == "ap":
            d = self.access_points
        if type == "firewall":
            d = self.firewalls
        if not d:
            return None
        
        if len(d) == 1:
            return d[0].name
        else:
            return f"{len(d)} Devices"
        

    def get_network_ids(self) -> list[str]:
        network_ids = []
        for net in self.networks:
            network_ids.append(net.id)
        return(network_ids)
    

    def clear_devices(self):
        self.access_points = None
        self.firewalls = None
        self.switches = None
