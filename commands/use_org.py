# Library Imports


# Local Imports
from sdk.models import Session, Command, ParsedCommand
from sdk.args import WildcardArg

from plugins.meraki.context import MerakiContext


def _use_org(session: Session, parsed_command: ParsedCommand):
    """Docstring for cmd function"""
    target_org = parsed_command.args[0]
    session.active_head.context.org = target_org.upper()


class UseOrg(Command):
    """Docstring for Cmd"""
    name = "use org"
    description = "Sets the active Organization in the Meraki Context"
    args = {WildcardArg}
    kwargs = None
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _use_org(session, parsed_command)
        return