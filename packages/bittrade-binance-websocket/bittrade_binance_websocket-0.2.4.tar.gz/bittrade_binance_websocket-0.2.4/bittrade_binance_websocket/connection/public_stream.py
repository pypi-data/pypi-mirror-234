from typing import Optional

from reactivex import ConnectableObservable
from reactivex.operators import publish
from reactivex.abc import SchedulerBase
import os
from elm_framework_helpers.websockets.models import WebsocketBundle

from bittrade_binance_websocket.connection.generic import raw_websocket_connection
from bittrade_binance_websocket.connection.reconnect import retry_with_backoff

URL = os.getenv('BINANCE_STREAM_WEBSOCKET', 'wss://stream.binance.com:443/ws/stream')

def public_websocket_connection(
    *, reconnect: bool = True, scheduler: Optional[SchedulerBase] = None
) -> ConnectableObservable[WebsocketBundle]:
    connection = raw_websocket_connection(URL, scheduler=scheduler)
    if reconnect:
        connection = connection.pipe(retry_with_backoff())
    return connection.pipe(publish())

__all__ = [
    "public_websocket_connection",
]
