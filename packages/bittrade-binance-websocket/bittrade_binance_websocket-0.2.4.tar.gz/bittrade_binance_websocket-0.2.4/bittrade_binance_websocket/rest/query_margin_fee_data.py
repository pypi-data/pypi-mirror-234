from typing import Any, Callable, Optional

from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models.rest import margin_account

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(list[margin_account.LeverageData])
def query_margin_fee_data_http_factory(
    symbol: str,
    is_isolated: Optional[bool] = False,
):
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.QUERY_ISOLATED_MARGIN_FEE_DATA
        if is_isolated
        else endpoints.BinanceEndpoints.QUERY_CROSS_MARGIN_FEE_DATA,
        params={"symbol": symbol},
    )
