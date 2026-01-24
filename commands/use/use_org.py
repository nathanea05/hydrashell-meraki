# Library Imports


# Hydrashell Imports
from sdk.models import Session, Command, ParsedCommand
from sdk.args import WildcardArg

# Local Imports
from ...core.context import MerakiContext
from ...models.organization import Organization


def _use_org(session: Session, ctx: MerakiContext, parsed_command: ParsedCommand):
    """Docstring for cmd function"""
    dashboard = ctx.dashboard
    response = dashboard.organizations.getOrganizations()

    target = parsed_command.args[0].strip().lower()

    organization = None
    for org in response:
        if str(org.get("name")).strip().lower() == target:
            organization = Organization.from_dict(org)
            break

    if organization:
        ctx.activate("org", organization)
    else:
        session.io.warn(f"Organization not found: {target}")
    return


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