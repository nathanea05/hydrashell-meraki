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


def _use_device(session: Session, ctx: MerakiContext, parsed_command: ParsedCommand):
    """Docstring for cmd function"""
    kwargs = parsed_command.kwargs


    dashboard = ctx.dashboard
    network_ids = ctx.get_network_ids()
    target = parsed_command.args[0].strip().lower()

    product_types = []
    if "switch" in kwargs:
        product_types.append("switch")
    if "wireless" in kwargs:
        product_types.append("wireless")
    if "appliance" in kwargs:
        product_types.append("appliance")

    if product_types:
        response = dashboard.organizations.getOrganizationDevices(organizationId=ctx.org.id, network_ids=network_ids, total_pages="all", product_types=product_types)
    else:
        response = dashboard.organizations.getOrganizationDevices(organizationId=ctx.org.id, network_ids=network_ids, total_pages="all")

    devices = []
    for dev in response:
        device = Device.from_dict(dev)

        if target in device.name.strip().lower() and device.network_id in network_ids:
            devices.append(device)
    
    if devices:
        ctx.devices = devices
        return
    
    raise InvalidCommand(f"Device not found: {target}")

    
class SwitchKwarg(Kwarg):
    name = "switch"
    description = "Will only select a switch"
    aliases = ["s"]


class WirelessKwarg(Kwarg):
    name = "wireless"
    description = "Will only select an Access Point"
    aliases = ["w"]


class ApplianceKwarg(Kwarg):
    name = "appliance"
    description = "Will only select an Appliance"
    aliases = ["fw"]


class UseDevice(Command):
    """Docstring for Cmd"""
    name = "use device"
    description = "Sets the active Device in the Meraki Context"
    args = {WildcardArg}
    kwargs = {SwitchKwarg, WirelessKwarg, ApplianceKwarg}
    required_context = {"org", "networks"}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _use_device(session, session.active_head.context, parsed_command)
        return