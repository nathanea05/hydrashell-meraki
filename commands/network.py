from sdk.models import Command, ParsedCommand, Session
from sdk.args import WildcardArg

def _network(session: Session, parsed_command: ParsedCommand):
    """Sets the active network in meraki context"""
    network = parsed_command.args[0]
    network = str(network).strip().lower()
    session.active_head.context.network = network


class NetworkCmd(Command):
    name = "network"
    description = "Sets the active network"
    args = {WildcardArg}
    kwargs = None
    required_context = {"org"}
    help = ""

    def execute(self, session, parsed_command):
        _network(session, parsed_command)
        return