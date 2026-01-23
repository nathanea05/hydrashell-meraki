# Library Imports


# Hydrashell Imports
from sdk.models import Session, Command, ParsedCommand, Kwarg
from sdk.args import WildcardArg
from sdk.exceptions import InvalidCommand

# Local Imports
from ...core.context import MerakiContext
from ...models.organization import Organization
from ...models.network import Network
from ...models.device import Device



def _use_device(session: Session, ctx: MerakiContext, parsed_command: ParsedCommand, product_type: str = None):
    """Docstring for cmd function"""

    dashboard = ctx.dashboard
    network_ids = ctx.get_network_ids()
    target = parsed_command.args[0].strip().lower()

    product_types = []
    product_types.append(product_type)
    if ctx.is_all_networks:
        response = dashboard.organizations.getOrganizationDevices(organizationId=ctx.org.id, total_pages="all", productTypes=product_types)
    else:
        response = dashboard.organizations.getOrganizationDevices(organizationId=ctx.org.id, networkIds=network_ids, total_pages="all", productTypes=product_types)

    devices = []
    for dev in response:
        device = Device.from_dict(dev)

        if target in device.name.strip().lower() and device.network_id in network_ids:
            devices.append(device)
    
    if devices:
        if product_type == "switch":
            ctx.switches = devices
            ctx.access_points = None
            ctx.firewalls = None
        if product_type == "wireless":
            ctx.access_points = devices
            ctx.switches = None
            ctx.firewalls = None
        if product_type == "appliance":
            ctx.firewalls = devices
            ctx.switches = None
            ctx.access_points = None
        return
    
    raise InvalidCommand(f"Device not found: {target}")



class UseSwitch(Command):
    """Docstring for Cmd"""
    name = "use switch"
    description = "Sets the active switch in the Meraki Context"
    args = {WildcardArg}
    kwargs = {}
    required_context = {"org", "networks"}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _use_device(session, session.active_head.context, parsed_command, product_type="switch")
        return
    

class UseAp(Command):
    """Docstring for Cmd"""
    name = "use ap"
    description = "Sets the active Access Point in the Meraki Context"
    args = {WildcardArg}
    kwargs = {}
    required_context = {"org", "networks"}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _use_device(session, session.active_head.context, parsed_command, product_type="wireless")
        return
    

class UseFirewall(Command):
    """Docstring for Cmd"""
    name = "use firewall"
    description = "Sets the active firewall in the Meraki Context"
    args = {WildcardArg}
    kwargs = {}
    required_context = {"org", "networks"}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _use_device(session, session.active_head.context, parsed_command, product_type="appliance")
        return