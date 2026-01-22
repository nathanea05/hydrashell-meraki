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
    dashboard = ctx.get_dashboard()
    response = dashboard.organizations.getOrganizationNetworks(organizationId=ctx.org.id)

    target = parsed_command.args[0].strip().lower()

    network = None

    for net in response:
        name = str(net.get("name", "")).strip().lower()
        if name == target:
            network = net
            break

    if network:
        ctx.network = Network.from_dict(network)
        return
    ctx.network = None
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