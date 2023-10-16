from logging import getLogger
import os
from typing import Any, Optional

from reactivex import ConnectableObservable
from reactivex.abc import SchedulerBase
from reactivex.operators import publish

from bittrade_binance_websocket.connection.reconnect import retry_with_backoff
from bittrade_binance_websocket.connection.generic import raw_websocket_connection

logger = getLogger(__name__)

WEBSOCKET_URL = os.getenv('BINANCE_WEBSOCKET_API', 'wss://ws-api.binance.com:443/ws-api/v3')


def private_websocket_connection(
    *, reconnect: bool = True, scheduler: Optional[SchedulerBase] = None
) -> ConnectableObservable[Any]:
    """You need to add your token to the EnhancedWebsocket
    An example implementation can be found in `examples/private_subscription.py`"""
    connection = raw_websocket_connection(url=WEBSOCKET_URL, scheduler=scheduler)
    if reconnect:
        connection = connection.pipe(retry_with_backoff())

    return connection.pipe(publish())


__all__ = [
    "private_websocket_connection",
]
