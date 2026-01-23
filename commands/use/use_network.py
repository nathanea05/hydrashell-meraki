# Library Imports


# Hydrashell Imports
from sdk.models import Session, Command, ParsedCommand
from sdk.args import WildcardArg
from sdk.exceptions import InvalidCommand

# Local Imports
from ...context import MerakiContext
from ...models.organization import Organization
from ...models.network import Network


def _use_network(session: Session, ctx: MerakiContext, parsed_command: ParsedCommand):
    """Docstring for cmd function"""
    kwargs = parsed_command.kwargs

    dashboard = ctx.dashboard
    response = dashboard.organizations.getOrganizationNetworks(organizationId=ctx.org.id)

    target = parsed_command.args[0].strip().lower()

    networks = []

    for net in response:
        network = Network.from_dict(net)
        
        if target == "all":
            networks.append(network)
            continue

        else:
            if network.name.strip().lower() == target:
                networks.append(network)
                break

    if networks:
        ctx.networks = networks
        if target == "all":
            ctx.all_networks = True
        else:
            ctx.all_networks = False
        return
    raise InvalidCommand(f"Network not found: {target}")
    


class UseNetwork(Command):
    """Docstring for Cmd"""
    name = "use network"
    description = "Sets the active Organization in the Meraki Context"
    args = {WildcardArg}
    kwargs = None
    required_context = {"org"}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _use_network(session, session.active_head.context, parsed_command)
        return