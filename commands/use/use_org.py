# Library Imports


# Hydrashell Imports
from sdk.models import Session, Command, ParsedCommand
from sdk.args import WildcardArg

# Local Imports
from ...context import MerakiContext
from ...models.organization import Organization


def _use_org(session: Session, ctx: MerakiContext, parsed_command: ParsedCommand):
    """Docstring for cmd function"""
    dashboard = ctx.get_dashboard()
    response = dashboard.organizations.getOrganizations()

    org = response[0]

    ctx.org = Organization.from_dict(org)
    ctx.network = None


class UseOrg(Command):
    """Docstring for Cmd"""
    name = "use org"
    description = "Sets the active Organization in the Meraki Context"
    args = {WildcardArg}
    kwargs = None
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _use_org(session, session.active_head.context, parsed_command)
        return