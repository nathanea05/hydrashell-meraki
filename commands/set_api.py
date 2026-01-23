from sdk.models import Command, Session, ParsedCommand
from ..core.context import MerakiContext
from ..core.init import dashboard_init


def _set_dashboard(session: Session, ctx: MerakiContext, parsed_command: ParsedCommand):
    dashboard_init(session=session, ctx=session.active_head.context)


class SetApi(Command):
    name = "set api"
    description = "Sets the active API key"
    args = None
    kwargs = None
    required_context = None
    help = ""


    def execute(self, session: Session, parsed_command: ParsedCommand):
        _set_dashboard(session, session.active_head.context, parsed_command)
        return