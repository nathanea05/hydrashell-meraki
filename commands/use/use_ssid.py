# Library Imports


# Hydrashell Imports
from sdk.models import Session, Command, ParsedCommand
from sdk.args import WildcardArg
from sdk.exceptions import InvalidCommand

# Local Imports
from ...core.context import MerakiContext
from ...models.ssid import Ssid


def _use_ssid(session: Session, ctx: MerakiContext, parsed_command: ParsedCommand):
    """Docstring for cmd function"""
    dashboard = ctx.dashboard
    args = parsed_command.args
    kwargs = parsed_command.kwargs

    search_term = None

    if args:
        search_term = str(args[0]).strip().lower()
    
    vlan_id = kwargs.get("vlan", None)
    if vlan_id:
        try:
            int(vlan_id)
        except:
            raise InvalidCommand("Ssid number must be an integer (Whole Number)")

    ssids = []
    network_ids = ctx.get_network_ids()
    for network_id in network_ids:
        response = dashboard.wireless.getNetworkWirelessSsids(network_id)

        for s in response:
            s["networkId"] = network_id
            ssid = Ssid.from_dict(s)

            name = ssid.name.strip().lower()
            

            if search_term:
                if search_term == "all":
                    ssids.append(ssid)
                    continue
                if search_term in name:
                    ssids.append(ssid)
                    continue
            if vlan_id:
                s_id = int(ssid.number)
                if vlan_id == s_id:
                    ssids.append(ssid)
                    continue


    if ssids:
        ctx.ssids = ssids
        ctx.clear_devices()
        ctx.vlans = None
        return
    session.io.warn("Ssid not found")





class UseSsid(Command):
    """Docstring for Cmd"""
    name = "use ssid"
    description = "Sets the active SSID in the Meraki Context"
    args = {WildcardArg}
    kwargs = None
    required_context = {"org", "networks"}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _use_ssid(session, session.active_head.context, parsed_command)
        return