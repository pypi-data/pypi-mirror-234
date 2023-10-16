from logging import getLogger
from typing import Any, Tuple, Dict, Literal, Union, List, Optional, TYPE_CHECKING

import orjson
import reactivex.disposable
from reactivex import Observable
from reactivex.abc import SchedulerBase, ObserverBase
from reactivex.scheduler import ThreadPoolScheduler
from websocket import WebSocketConnectionClosedException, WebSocketApp
from elm_framework_helpers.websockets.models import (
    WebsocketBundle,
    WEBSOCKET_MESSAGE,
    WEBSOCKET_HEARTBEAT,
    WEBSOCKET_STATUS,
    WEBSOCKET_OPENED,
    WEBSOCKET_CLOSED,
)

from bittrade_binance_websocket.models import EnhancedWebsocket


logger = getLogger(__name__)
raw_logger = getLogger("bittrade_binance_websocket.raw_socket.received")


def raw_websocket_connection(
    url: str, scheduler: Optional[SchedulerBase] = None
) -> Observable[WebsocketBundle]:
    def subscribe(
        observer: ObserverBase[WebsocketBundle],
        scheduler_: Optional[SchedulerBase] = None,
    ):
        _scheduler = scheduler or scheduler_ or ThreadPoolScheduler()
        connection: WebSocketApp | None = None

        def action(*args: Any):
            nonlocal connection

            def on_error(_ws: WebSocketApp, error: Exception):
                logger.error("[SOCKET][RAW] Websocket errored %s", error)
                observer.on_next((enhanced, WEBSOCKET_STATUS, WEBSOCKET_CLOSED))
                observer.on_error(error)

            def on_close(_ws: WebSocketApp, close_status_code: int, close_msg: str):
                logger.warning(
                    "[SOCKET][RAW] Websocket closed | url: %s, status: %s, close message: %s",
                    url,
                    close_status_code,
                    close_msg,
                )
                observer.on_next((enhanced, WEBSOCKET_STATUS, WEBSOCKET_CLOSED))
                observer.on_error(Exception("Socket closed"))

            def on_open(_ws: WebSocketApp):
                logger.info("[SOCKET][RAW] Websocket opened at %s", url)
                observer.on_next((enhanced, WEBSOCKET_STATUS, WEBSOCKET_OPENED))

            def on_message(ws: WebSocketApp, message: bytes | str):
                pass_message = orjson.loads(message)
                category = WEBSOCKET_MESSAGE
                raw_logger.debug(message)
                logger.debug("[SOCKET][RAW] %s", message)

                try:
                    observer.on_next((enhanced, category, pass_message))
                except:
                    logger.exception("[SOCKET] Error on socket message")

            connection = WebSocketApp(
                url,
                on_open=on_open,
                on_close=on_close,
                on_error=on_error,
                on_message=on_message,
            )
            enhanced = EnhancedWebsocket(connection)

            def run_forever(*args: Any):
                assert connection is not None
                connection.run_forever()

            _scheduler.schedule(run_forever)

        def disconnect():
            logger.info("[SOCKET] Releasing resources")
            assert connection is not None
            try:
                connection.close()
            except WebSocketConnectionClosedException as exc:
                logger.error("[SOCKET] Socket was already closed %s", exc)

        return reactivex.disposable.CompositeDisposable(
            _scheduler.schedule(action), reactivex.disposable.Disposable(disconnect)
        )

    return Observable(subscribe)


__all__ = ["raw_websocket_connection"]
