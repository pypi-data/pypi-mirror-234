from logging import getLogger
import os
from typing import Any, Callable, Optional

from reactivex import ConnectableObservable, Observable
from reactivex.disposable import CompositeDisposable
import reactivex
from reactivex.abc import SchedulerBase
from reactivex.operators import publish

from elm_framework_helpers.operators.retry_with_delay import (
    retry_with_delay,
    binance_delay,
)
from elm_framework_helpers.websockets.models import WebsocketBundle
from reactivex import operators, abc
from bittrade_binance_websocket.connection.generic import raw_websocket_connection
from bittrade_binance_websocket.models.rest.listen_key import CreateListenKeyResponse

logger = getLogger(__name__)

USER_URL = os.getenv("BINANCE_USER_WEBSOCKET", "wss://stream.binance.com:9443/ws")


def private_websocket_user_stream(
    listen_key_getter: Callable[[], Observable[CreateListenKeyResponse]],
    listen_key_keep_alive: Callable[[str], Observable[None]],
) -> ConnectableObservable[WebsocketBundle]:
    return private_websocket_user_stream_(
        raw_websocket_connection,
        listen_key_getter,
        listen_key_keep_alive,
        reactivex.interval(600),
    )


def private_websocket_user_stream_(
    websocket_connection: Callable[[str], Observable[WebsocketBundle]],
    listen_key_getter: Callable[[], Observable[CreateListenKeyResponse]],
    listen_key_keep_alive: Callable[[str], Observable[None]],
    listen_key_keep_alive_interval: Observable[int],
) -> ConnectableObservable[WebsocketBundle]:
    def subscribe(
        observer: abc.ObserverBase, scheduler: Optional[SchedulerBase] = None
    ) -> abc.DisposableBase:
        listen_key = ""
        sub = CompositeDisposable()

        try:
            listen_key = listen_key_getter().run()["listenKey"]
        except:
            logger.exception("Failed to get listen key")
            observer.on_error("Failed to get listen key")
            return
        # Start the keep alive process
        sub.add(
            listen_key_keep_alive_interval.pipe(
                operators.flat_map(lambda _: listen_key_keep_alive(listen_key))
            ).subscribe(
                on_next=lambda _: logger.debug("Keep alive sent"),
                on_error=lambda e: observer.on_error(e),
                on_completed=lambda: observer.on_error(
                    "Keep alive stopped; terminating connection"
                ),
                scheduler=scheduler,
            )
        )
        url = f"{USER_URL}/{listen_key}"
        connection = websocket_connection(url=url, scheduler=scheduler)
        sub.add(connection.subscribe(observer, scheduler=scheduler))
        return sub

    return Observable(subscribe).pipe(
        retry_with_delay(binance_delay(), reactivex.timer(3)), publish()
    )


__all__ = [
    "private_websocket_user_stream",
]
