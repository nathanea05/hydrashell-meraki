from dataclasses import dataclass
from sdk.models import Context, Session, ParsedCommand
from sdk.exceptions import ExitError


@dataclass
class MerakiContext(Context):

    org: str = None
    network: str = None


    def get_prompt(self):
        prompt = ""
        if self.org:
            prompt = self.org
        if self.network:
            prompt = f"{prompt}\\{self.network}"
        return prompt
    

    def use(self, session: Session, parsed_command: ParsedCommand):
        """Sets the active resource"""

            

    def exit(self):
        if self.network:
            self.network = None
            return
        if self.org:
            self.org = None
            return
        raise ExitError
        

    
    def set_org(self, org):
        """Sets the active org"""
        self.org = org


    def set_net(self, network):
        """Sets the active network"""
        self.network = network


