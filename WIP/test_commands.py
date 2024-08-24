import listeners.commands as commands
import unittest


def test_echo():
    assert commands.echo("Hello World") == "Hello World"


def test_send():
    assert commands.send("Hello World") == "Hello World"


def test_random():
    assert commands.random() == "Hello World"


if __name__ == "__main__":
    unittest.main()
# [functions]
# ack: slack_bolt.context.ack.ack.Ack
# client: slack_sdk.web.client.WebClient
# context: slack_bolt.context.context.BoltContext
# logger : logging.Logger
# next_:
# next:
# req: slack_bolt.request.request.BoltRequest
# request: slack_bolt.request.request.BoltRequest
# resp: slack_bolt.response.response.BoltResponse
# respond: slack_bolt.context.respond.respond.Respond
# response: slack_bolt.response.response.BoltResponse
# say: slack_bolt.context.say.say.Say

# [body]
# action: @app.action
# body : request body
# {'token': 'xxx', 'team_id': 'Txx', 'team_domain': 'xxx', 'channel_id': 'Cxx', 'channel_name': 'xxx', 'user_id': 'Uxx', 'user_name': 'email_id', 'command': '/random', 'api_app_id': 'Axx', 'is_enterprise_install': 'false', 'response_url': 'https://hooks.slack.com/commands/Txx/###/xxx', 'trigger_id': '###.###.xxx'}
# command: @app.command
# event: @app.event
# message: @app.message
# options: @app.options
# payload: request body
# shortcut: @app.shortcut
# view: @app.view
