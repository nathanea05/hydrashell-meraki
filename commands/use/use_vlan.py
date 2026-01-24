# Library Imports


# Hydrashell Imports
from sdk.models import Session, Command, ParsedCommand, Kwarg
from sdk.args import WildcardArg
from sdk.exceptions import InvalidCommand

# Local Imports
from ...core.context import MerakiContext
from ...models.vlan import Vlan


def _use_vlan(session: Session, ctx: MerakiContext, parsed_command: ParsedCommand):
    """Docstring for cmd function"""
    kwargs = parsed_command.kwargs
    dashboard = ctx.dashboard
    network_ids = ctx.get_network_ids()

    if parsed_command.args:
        target = parsed_command.args[0].strip().lower()
    else:
        target = None

    name = kwargs.get("name", None)
    vlan_id = kwargs.get("id", None)
    if vlan_id:
        try:
            int(vlan_id)
        except:
            raise InvalidCommand("id must be an integer (Whole Number)")

    vlans = []
    for network_id in network_ids:
        response = dashboard.appliance.getNetworkApplianceVlans(networkId=network_id)
        for v in response:
            v["network_id"] = network_id
            vlan = Vlan.from_dict(v)



            if target:
                if target == "all":
                    vlans.append(vlan)
                    continue
                if target in vlan.name.strip().lower():
                    vlans.append(vlan)
                    continue

            if name:
                if name in vlan.name.strip().lower():
                    vlans.append(vlan)
                    continue

            if vlan_id:
                if int(vlan_id) == int(vlan.id):
                    vlans.append(vlan)
                    continue

    if vlans:
        ctx.activate("vlan", vlans)
    else:
        session.io.warn(f"Vlan not found: {target}")
    return



class NameKwarg(Kwarg):
    name = "name"
    description = "Filter vlans by name"
    aliases = "n"

class IdKwarg(Kwarg):
    name = "id"
    description = "Filter vlans by  Vlan ID"


class UseOrg(Command):
    """Docstring for Cmd"""
    name = "use vlan"
    description = "Sets the active Organization in the Meraki Context"
    args = {WildcardArg}
    kwargs = {NameKwarg, IdKwarg}
    required_context = {"org", "network"}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _use_vlan(session, session.active_head.context, parsed_command)
        return