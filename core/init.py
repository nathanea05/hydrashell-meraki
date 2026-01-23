# Library Imports
import meraki
from meraki.exceptions import APIError

# Hydrashell Imports
from sdk.models import HeadInit, Session
from sdk.exceptions import ExitHead

# Local Imports
from .context import MerakiContext


def dashboard_init(session: Session, ctx: MerakiContext) -> meraki.DashboardAPI:
    """Initializes and validates the Meraki Dashboard API client"""
    old_db = ctx.dashboard

    while True:
        api_key = session.services.authentication.get_api_key()
        if not api_key:
            raise ExitHead("No API Key")

        dashboard = meraki.DashboardAPI(
            api_key,
            output_log=False,
        )

        try:
            # This call is cheap and requires valid auth
            dashboard.organizations.getOrganizations()

        except APIError as e:
            status = getattr(e, "status", None)
            body = getattr(e, "body", None)

            # 401 / 403 = invalid or unauthorized key
            if status in (401, 403):
                session.io.warn("Invalid or unauthorized Meraki API key.")

            # 429 = rate limit (valid key, just throttled)
            elif status == 429:
                session.io.warn("Meraki API rate limit exceeded. Try again shortly.")

            else:
                session.io.warn(
                    f"Failed to initialize Meraki dashboard "
                    f"(HTTP {status}): {body or e}"
                )

            if session.io.confirm("Would you like to try again?"):
                continue
            else:
                if old_db:
                    return
                raise ExitHead("Failed to authenticate Meraki API")

        # success
        ctx.dashboard = dashboard
        return dashboard


class MerakiInit(HeadInit):
    def init(self, session: Session) -> bool:
        dashboard = dashboard_init(session, session.active_head.context)