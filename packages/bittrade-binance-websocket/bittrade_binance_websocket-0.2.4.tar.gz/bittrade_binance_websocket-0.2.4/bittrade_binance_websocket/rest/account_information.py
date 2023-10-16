from typing import Any, Callable

from reactivex import Observable, just, throw
from reactivex import operators
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models import order

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(dict)
def get_account_information_http_factory(
    isolated: bool = False, symbols: list[str] | None = None
):
    params = {}
    if isolated and symbols:
        params["symbols"] = ",".join(symbols)
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.MARGIN_ACCOUNT_INFORMATION
        if isolated
        else endpoints.BinanceEndpoints.ACCOUNT_INFORMATION,
        params=params,
    )
