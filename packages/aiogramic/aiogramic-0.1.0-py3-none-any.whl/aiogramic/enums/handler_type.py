from enum import StrEnum


class HandlerType(StrEnum):

    MESSAGE = "message"
    CALLBACK_QUERY = "callback_query"
    CHAT_MEMBER = "chat_member"
    MY_CHAT_MEMBER = "my_chat_member"
    CHANNEL_POST = "channel_post"
    EDITED_MESSAGE = "edited_message"
    EDITED_CHANNEL_POST = "edited_channel_post"
