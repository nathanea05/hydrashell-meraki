from sdk.models import Command, Session, ParsedCommand
from ..context import MerakiContext
from ..models.device import Device


def _get_devices(session: Session, ctx: MerakiContext, parsed_command: ParsedCommand):
    db = ctx.dashboard
    devices = []

    if ctx.networks and not ctx.is_all_networks:
        network_ids = ctx.get_network_ids()
        response = db.organizations.getOrganizationDevices(ctx.org.id, networkIds=network_ids)

    else:
        response = db.organizations.getOrganizationDevices(ctx.org.id)


    for dev in response:
        device = Device.from_dict(dev)
        devices.append(device)
    session.io.pwrite(devices)


class GetDevices(Command):
    name = "get devices"
    description = "Gets all devices in an organization"
    args = None
    kwargs = None
    required_context = {"org"}
    help = ""


    def execute(self, session: Session, parsed_command: ParsedCommand):
        _get_devices(session, session.active_head.context, parsed_command)
        return