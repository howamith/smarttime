from datetime import timedelta

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from calendar_service import CalendarService
import slack_tokens

app = App(token=slack_tokens.BOT)
HOURS = 1
MINUTES = 30


def get_user_email(user_id: str) -> str:
    return app.client.users_info(user=user_id)["user"]["profile"]["email"]


@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")


@app.command("/focus-time")
def focus_time(ack, respond, command):
    ack()

    service = CalendarService(get_user_email(command["user_id"]))
    opportunities = service.get_focus_time_opportunities(
        timedelta(hours=HOURS, minutes=MINUTES)
    )

    message = ""
    for date in opportunities:
        opps = "\n  ".join(opportunities[date])
        message += f"\n {date}:\n  {opps}"
    respond(f"You have opportunites for focus time: {message}")


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, slack_tokens.APP).start()
