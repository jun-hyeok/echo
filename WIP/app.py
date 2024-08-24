import os
import yaml
from slack_bolt import App

file = open("functions/.env.yaml")
secrets = yaml.safe_load(file)
file.close()
app = App(
    token=secrets.get("SLACK_BOT_TOKEN"),
    signing_secret=secrets.get("SLACK_SIGNING_SECRET"),
)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
# TODO
# WEB API -> act
# - views.open, update, push : dynamic
# - views.publish : static
# - users.identity[u], user.info[b|u], users.profile.get[b|u] : info
# - users.list : all users
# - users.lookupByEmail : search by email
## identity:basic, uers:read.profile email, channels:read, groups:read, im:read, mpim:read
# - reactions.add, get, list, remove
## reactions:write, read,
# - files.upload : gif?
## files:write
# - dialog.open : knowledge?
# - conversations.history, info, invite, members, replies
## *:history, *:read, *:write,
# - chat.update, unfurl, scheduleMessage, postMessage, postEphemeral, meMessage, getPermalink, deleteScheduledMessage, delete
## chat:write, links:write
# - bot.info
## users:read
# - admin for Enterprise
# Event API -> read


# @app.event("message")
# def handle_message_events(body, logger, message, say):
#     logger.info(body)
#     say(f"{message['text']}")


# @app.event(
#     {
#         "type": "app_mention",
#     }
# )
# def user_list(client, say):
#     channel = say.channel
#     users = client.conversations_members(
#         token=secrets.get("SLACK_BOT_TOKEN"), channel=channel
#     )
#     text = ", ".join(list(map(lambda u: f"<@{u}>", users["members"])))
#     say(text=text)


# @app.message("hello")
# def message_hello(message, say):
#     # say() sends a message to the channel where the event was triggered
#     say(
#         blocks=[
#             {
#                 "type": "section",
#                 "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
#                 "accessory": {
#                     "type": "button",
#                     "text": {"type": "plain_text", "text": "Click Me"},
#                     "action_id": "button_click",
#                 },
#             }
#         ],
#         text=f"Hey there <@{message['user']}>!",
#     )


# @app.action("button_click")
# def action_button_click(body, ack, say):
#     # Acknowledge the action
#     ack()
#     say(f"<@{body['user']['id']}> clicked the button")
