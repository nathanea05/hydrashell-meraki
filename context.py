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


def dashboard_init(api_key: str) -> meraki.DashboardAPI:
    """Initializes the meraki dashboard"""
    


@dataclass
class MerakiContext(Context):

    dashboard: Optional[meraki.DashboardAPI] = None
    org: Optional[Organization] = None
    network: Optional[Network] = None


    def get_prompt(self):
        prompt = ""
        if self.org:
            prompt = self.org.name
        if self.network:
            prompt = f"{prompt}\\{self.network.name}"
        return prompt
            

    def exit(self):
        if self.network:
            self.network = None
            return
        if self.org:
            self.org = None
            return
        raise ExitHead
        

    def get_dashboard(self):
        if self.dashboard:
            return self.dashboard
        api_key = getpass("Enter your Meraki API Key: ")
        self.dashboard = meraki.DashboardAPI(api_key, output_log=False)
        return self.dashboard
        

    
    def set_org(self, org: Organization):
        """Sets the active org"""
        self.org = org


    def set_net(self, network):
        """Sets the active network"""
        self.network = network


