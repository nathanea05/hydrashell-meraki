from sdk.models import Command, Session, ParsedCommand

class TestCmd(Command):
    name = "test"
    description = "test command"
    args = None
    kwargs = None
    required_context = {"org"}
    help = ""


    def execute(self, session: Session, parsed_command: ParsedCommand):
        print("Success!")
        return