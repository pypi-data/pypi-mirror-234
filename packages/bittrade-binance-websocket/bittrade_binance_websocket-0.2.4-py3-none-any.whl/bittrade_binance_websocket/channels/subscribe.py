from logging import getLogger
from typing import Any, Callable, Dict, List, Mapping, Optional
import typing

from reactivex import Observable, operators, compose
from reactivex.abc import ObserverBase, SchedulerBase
from reactivex.disposable import CompositeDisposable, Disposable

from .message import make_sub_unsub_messages

from bittrade_binance_websocket.models import (
    UserFeedMessage,
    EnhancedWebsocket,
    ResponseMessage,
)
from bittrade_binance_websocket.messages.filters.kind import keep_channel_messages
from elm_framework_helpers.output import info_operator
from expression import curry_flip

logger = getLogger(__name__)


@curry_flip(1)
def channel_subscription(
    source: Observable[ResponseMessage],
    socket: EnhancedWebsocket,
    channel: str,
    unsubscribe_on_dispose: bool,
) -> Observable[UserFeedMessage]:
    def subscribe(observer: ObserverBase, scheduler: Optional[SchedulerBase] = None):
        subscription_message, unsubscription_message = make_sub_unsub_messages(channel)
        socket.send_message(subscription_message)

        def on_exit():
            if unsubscribe_on_dispose:
                # We may be disconnected
                try:
                    socket.send_message(unsubscription_message)
                except Exception:
                    pass

        return CompositeDisposable(
            source.subscribe(observer, scheduler=scheduler),
            Disposable(action=on_exit),
        )

    return Observable(subscribe)


def subscribe_to_channel(
    messages: Observable[ResponseMessage],
    channel: str,
    unsubscribe_on_dispose: bool = True,
) -> Callable[[Observable[EnhancedWebsocket]], Observable[UserFeedMessage]]:
    def socket_to_channel_messages(
        socket: EnhancedWebsocket,
    ) -> Observable[UserFeedMessage]:
        return messages.pipe(
            keep_channel_messages(channel),
            channel_subscription(socket, channel, unsubscribe_on_dispose),
            # operators.map(_log),
        )

    return compose(
        operators.map(socket_to_channel_messages),
        operators.switch_latest(),
        operators.share(),
    )
