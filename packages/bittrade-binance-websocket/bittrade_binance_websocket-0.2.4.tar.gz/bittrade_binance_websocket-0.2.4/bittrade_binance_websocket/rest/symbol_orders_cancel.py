from typing import Any, Callable

from reactivex import Observable, just, throw
from reactivex import operators
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models import order

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(list[order.SymbolOrderResponseItem])
def delete_symbol_order_http_factory(params: order.SymbolOrdersCancelRequest):
    return request.RequestMessage(
        method="DELETE",
        endpoint=endpoints.BinanceEndpoints.MARGIN_OPEN_ORDERS
        if params.is_margin
        else endpoints.BinanceEndpoints.SPOT_OPEN_ORDERS,
        params=params.to_dict(),
    )


def is_empty_order_code(code: int):
    return code in [-2011]


def accept_empty_orders_list() -> Callable[[Observable[Any]], Observable[bool]]:
    """Operator that catches Binance's -2011 error which is sent when there are no orders to cancel."""

    def is_ok(err, src):
        try:
            code = err.response.json()["code"]
            if is_empty_order_code(code):
                return just([])
        except:
            pass
        return throw(err)

    return operators.catch(is_ok)
