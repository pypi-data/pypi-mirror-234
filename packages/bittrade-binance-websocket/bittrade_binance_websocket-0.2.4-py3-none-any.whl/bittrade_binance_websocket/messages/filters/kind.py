from reactivex import operators
from typing import TYPE_CHECKING, Callable
from reactivex import Observable
from bittrade_binance_websocket.models import UserFeedMessage, ResponseMessage


def _is_channel_message(channel: str):
    # channel is both symbol + event/channel type
    symbol = channel.split('@')[0]
    def channel_message_filter(x: UserFeedMessage):
        return x.get("s", "") == symbol.upper()

    return channel_message_filter


def keep_channel_messages(
    channel: str,
) -> Callable[[Observable[ResponseMessage]], Observable[UserFeedMessage]]:
    return operators.filter(_is_channel_message(channel))
