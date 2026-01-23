# Library Imports
import meraki
from dataclasses import dataclass
from typing import Optional
from getpass import getpass

# Hydrashell Imports
from sdk.models import Context, Session, ParsedCommand
from sdk.exceptions import ExitHead

# Local Imports
from .models.organization import Organization
from .models.network import Network
from .models.device import Device


def dashboard_init(api_key: str) -> meraki.DashboardAPI:
    """Initializes the meraki dashboard"""
    


@dataclass
class MerakiContext(Context):

    dashboard: Optional[meraki.DashboardAPI] = None
    org: Optional[Organization] = None
    networks: Optional[list[Network]] = None
    is_all_networks: Optional[bool] = False
    devices: Optional[set[Device]] = None


    def get_prompt(self):
        parts = []

        if self.org:
            parts.append(self.org.name)


        if self.networks:
            parts.append(self.repr_networks())

        if self.devices:
            parts.append(self.repr_devices())

        
        return "\\".join(parts)

            

    def exit(self):
        if self.devices:
            self.devices = None
        if self.networks:
            self.networks = None
            return
        if self.org:
            self.org = None
            return
        raise ExitHead


    def repr_networks(self) -> str:
        n = self.networks

        if not n:
            return None
        
        if len(n) == 1:
            return n[0].name
        
        if len(n) > 1:
            return f"{len(n)} Networks"
        
    
    def repr_devices(self) -> str:
        d = self.devices

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
