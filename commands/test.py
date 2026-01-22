from sdk.models import Command

class TestCmd(Command):
    name = "test"
    description = "test command"
    args = None
    kwargs = None
    required_context = {"org"}
    help = ""


    def execute(self, session, parsed_command):
        print("Success!")
        return