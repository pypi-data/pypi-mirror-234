from typing import Any, Callable

from reactivex import Observable, just, throw
from reactivex import operators
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models import order

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(list[order.SymbolOrderResponseItem])
def open_orders_http_factory(params: order.SymbolOrdersCancelRequest):
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.MARGIN_OPEN_ORDERS
        if params.is_margin
        else endpoints.BinanceEndpoints.SPOT_OPEN_ORDERS,
        params=params.to_dict(),
    )
