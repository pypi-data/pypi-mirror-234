from typing import Any, Callable, Optional

from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models.rest import margin_account

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(margin_account.AccountInfo)
def query_margin_account_details_http_factory(
    is_isolated: Optional[bool] = False,
):
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.QUERY_ISOLATED_MARGIN_ACCOUNT_DETAILS
        if is_isolated
        else endpoints.BinanceEndpoints.QUERY_CROSS_MARGIN_ACCOUNT_DETAILS,
    )
