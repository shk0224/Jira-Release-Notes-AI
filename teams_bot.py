
"""Microsoft Teams integration for Jira Release Notes AI."""

from microsoft_teams.apps import App, FastAPIAdapter


def create_teams_bot(fastapi_app):
    """Connect Microsoft Teams to the existing FastAPI application."""

    adapter = FastAPIAdapter(app=fastapi_app)
    teams_app = App(http_server_adapter=adapter)

    @teams_app.on_message
    async def handle_message(ctx):
        """Receive a Teams message and send a response."""

        user_message = (ctx.activity.text or "").strip()

        if not user_message:
            await ctx.send(
                "Please enter a Jira project and fix version."
            )
            return

        await ctx.send(
            f"Received your request: {user_message}\n\n"
            "Teams connection is ready for backend integration. "
            "Release notes have not been generated yet."
        )

    return teams_app
