from typing import Callable, Dict, List, cast

from reactivex import Observable, compose, operators, timer

from elm_framework_helpers.websockets import models
from elm_framework_helpers.websockets.operators import connection_operators
from elm_framework_helpers.websockets.models import WebsocketBundle, WEBSOCKET_MESSAGE, WEBSOCKET_HEARTBEAT, WEBSOCKET_STATUS, WEBSOCKET_OPENED, WEBSOCKET_CLOSED

from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket

def filter_new_socket_only() -> Callable[[Observable[WebsocketBundle]], Observable[EnhancedWebsocket]]:
    return compose(
        operators.map(lambda x: x[0]),
        operators.distinct_until_changed(), # type: ignore
    )