from sdk.models import Alias


class Org(Alias):
    name = "org"
    executes = "use org"
    description = "Sets the active organization"