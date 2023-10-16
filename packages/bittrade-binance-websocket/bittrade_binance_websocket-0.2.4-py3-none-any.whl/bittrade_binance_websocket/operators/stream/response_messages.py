from typing import Callable, cast
from reactivex import Observable, compose, operators
from elm_framework_helpers.websockets.operators import connection_operators
from bittrade_binance_websocket.models.response_message import ResponseMessage


def keep_messages_only():
    return compose(
        connection_operators.keep_messages_only(),
        operators.map(lambda x: cast(ResponseMessage, x)),
    )


def keep_response_messages_only():
    def is_response(x: ResponseMessage):
        return x.id != -1

    return operators.filter(is_response)


def exclude_response_messages():
    def is_response(x: ResponseMessage):
        return x.id == -1

    return operators.filter(is_response)
