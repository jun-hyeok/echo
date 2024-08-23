import logging
from typing import Any, Dict

import utils.models as m
from slack_bolt import Ack, Say


def preview_poll(
    body: Dict[str, Any],
    logger: logging.Logger,
    view: Dict[str, Any],
    ack: Ack,
):
    """
    preview a poll from the view submission

    settings (int): (0 ~ 15)
        - anonymous (0b0001): multiple choice
        - add_option_allowed (0b0010): anonymous vote
        - add_option_allowed (0b0100): add options allowed
        - add_option_allowed (0b1000): set deadlines
    """
    logger.info(body)

    state_values = view["state"]["values"]

    channel = state_values["channel"]["select"]["selected_conversation"]
    title = state_values["title"]["input"]["value"]
    options = state_values["options"]["input"]["value"].splitlines()
    settings = state_values["settings"]["checkboxes"]["selected_options"]
    settings = sum(eval(setting["value"]) for setting in settings)

    blocks = [
        m.Context(elements=[m.mrkdwn(text=f"<#{channel}>")]),
        m.Section(block_id="title", text=m.mrkdwn(text=f"*{title}*")),
        m.Divider(),
        *(
            m.Section(
                block_id=f"option_{i+1}", text=m.mrkdwn(text=f"{i+1}. {option}\n`0` ")
            )
            for i, option in enumerate(dict.fromkeys(filter(None, options)).keys())
        ),
        m.Divider(),
        m.Context(elements=[m.mrkdwn(text=f"<@{body['user']['id']}>님이 투표를 실행하였습니다.")]),
    ]
    ack(
        response_action="push",
        view=m.View(
            type="modal",
            callback_id="create_poll",
            title=m.plain_text(text="투표 미리보기"),
            submit=m.plain_text(text="투표 올리기"),
            close=m.plain_text(text="취소"),
            blocks=blocks,
            private_metadata=f"{channel}.{settings}.{title}",
        ),
    )


def create_poll(
    body: Dict[str, Any],
    logger: logging.Logger,
    view: Dict[str, Any],
    ack: Ack,
    say: Say,
):
    """
    make a poll from the view submission
    """
    logger.info(body)

    channel, settings, title = view["private_metadata"].split(".")

    metadata = m.metadata(
        event_type="poll",
        event_payload={
            "channel": channel,
            "settings": settings,
            "title": title,
        },
    )

    overflow = m.overflow(
        action_id="poll_overflow",
        options=[
            m.option(
                text=m.plain_text(text=":lock: 투표 종료", emoji=True),
                value="end_poll",
            ),
            m.option(
                text=m.plain_text(text=":no_entry: 투표 취소", emoji=True),
                value="cancel_poll",
            ),
        ],
    ).to_dict()

    # poll settings
    if int(settings) & 0b0001:
        pass
    else:
        # single choice
        pass
    if int(settings) & 0b0010:
        action_id = "vote_anonymous"
    else:
        action_id = "vote"
    if int(settings) & 0b0100:
        # add options allowed
        pass
    if int(settings) & 0b1000:
        # set deadlines
        pass

    blocks = view["blocks"]
    _, *blocks = blocks

    title = blocks[0]
    title.update(accessory=overflow)

    options = blocks[2:-2]
    for i, option in enumerate(options):
        option.update(
            accessory=m.button(
                action_id=action_id,
                text=m.plain_text(text=f"{i+1}"),
                value=f"{i+1}",
            ).to_dict(),
        )

    ack(response_action="clear")
    say(
        username="투표",
        icon_emoji=":bar_chart:",
        channel=channel,
        blocks=blocks,
        metadata=metadata,
    )
