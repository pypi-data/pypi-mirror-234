from reactivex import compose, operators

from elm_framework_helpers.websockets.operators.connection_operators import (
    keep_messages_only,
)


def is_open_order_message(x: dict) -> bool:
    return x.get("e", "") == "executionReport"


def keep_open_orders_messages():
    """Use with a WebsocketBundle feed"""
    return compose(keep_messages_only(), operators.map(is_open_order_message))


__all__ = ["keep_open_orders_messages"]
