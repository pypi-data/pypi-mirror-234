from typing import Any, Callable, Optional

from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models import order

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(order.SymbolOrderResponseItem)
def create_order_http_factory(
    params: order.PlaceOrderRequest,
):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.MARGIN_ORDER
        if params.is_margin
        else endpoints.BinanceEndpoints.SPOT_ORDER,
        params=params.to_dict(),
    )
