# might be good to move to elm-framework-helpers

from logging import getLogger
from typing import Any, Callable, Dict, List, TypeVar, cast
from reactivex import Observable, compose, operators
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket

from bittrade_binance_websocket.models.response_message import ResponseMessage

R = TypeVar("R")

logger = getLogger(__name__)


class RequestResponseError(Exception):
    pass


def add_keys(
    secret: str, key: str
) -> Callable[[Observable[EnhancedWebsocket]], Observable[EnhancedWebsocket]]:
    def _set_token(socket: EnhancedWebsocket):
        socket.key = key
        socket.secret = secret
        return socket

    return operators.map(_set_token)


def is_match(id: str):
    def _is_match(message: R):
        msg = cast(Dict[str, str], message)
        msg_id = msg.get("id")
        return id == msg_id

    return _is_match


def wait_for_response(
    id: str, timeout: float
) -> Callable[[Observable[R]], Observable[R]]:
    return compose(
        operators.filter(is_match(id)),
        operators.do_action(
            on_next=lambda x: logger.debug("[SOCKET] Received matching message")
        ),
        operators.take(1),  # take only one message that fits the filter
        operators.timeout(timeout),
    )


def _response_ok(
    response: R, good_status: Any = "ok", bad_statuses: List[Any] = ["error"]
):
    r = cast(Dict, response)
    try:
        if r["status"] in bad_statuses:
            raise RequestResponseError(r["error"])
        elif r["status"] == good_status:
            return response
        raise RequestResponseError("Unknown status")
    except KeyError:
        raise Exception("Unknown response type")


def response_ok(
    good_status=200, bad_statuses=[400, 409]
) -> Callable[[Observable[R]], Observable[R]]:
    return operators.map(
        lambda response: _response_ok(response, good_status, bad_statuses)
    )
