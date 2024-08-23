import logging
from typing import Any, Dict

import slack_sdk
import utils.models as m
from slack_bolt import Ack


def poll(
    body: Dict[str, Any],
    logger: logging.Logger,
    client: slack_sdk.web.client.WebClient,
    ack: Ack,
):
    """
    make a poll
    """
    logger.info(body)

    ack()
    blocks = [
        m.Input(
            block_id="channel",
            label=m.plain_text(text=":hash: 채널", emoji=True),
            element=m.conversations_select(
                action_id="select",
                default_to_current_conversation=True,
                placeholder=m.plain_text(text="채널 선택"),
                filter=m.filter(
                    include=["public", "private", "mpim"],
                    exclude_bot_users=True,
                ),
            ),
        ),
        m.Divider(),
        m.Input(
            block_id="title",
            label=m.plain_text(text=":ballot_box_with_ballot: 투표 제목", emoji=True),
            element=m.plain_text_input(action_id="input"),
        ),
        m.Input(
            block_id="options",
            label=m.plain_text(text="항목"),
            element=m.plain_text_input(
                action_id="input",
                multiline=True,
                placeholder=m.plain_text(text="항목을 입력하세요. (한 줄에 하나씩)"),
            ),
        ),
        m.Input(
            block_id="settings",
            label=m.plain_text(text=" "),
            element=m.checkboxes(
                action_id="checkboxes",
                options=[
                    m.option(
                        text=m.plain_text(text="복수선택"),
                        value="0b0001",
                    ),
                    m.option(
                        text=m.plain_text(text="익명투표"),
                        value="0b0010",
                    ),
                    m.option(
                        text=m.plain_text(text="선택항목 추가 허용"),
                        value="0b0100",
                    ),
                    m.option(
                        text=m.plain_text(text="마감시간 설정"),
                        value="0b1000",
                    ),
                ],
            ),
            optional=True,
        ),
    ]
    client.views_open(
        trigger_id=body["trigger_id"],
        view=m.View(
            type="modal",
            callback_id="preview_poll",
            title=m.plain_text(text="투표 올리기"),
            submit=m.plain_text(text="미리보기"),
            close=m.plain_text(text="취소"),
            blocks=blocks,
        ),
    )
