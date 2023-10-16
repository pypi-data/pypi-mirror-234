from typing import Any, Callable, Optional

from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models import loan

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(loan.AccountBorrowRequest)
def account_borrow_http_factory(
    params: loan.AccountBorrowRequest,
):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.MARGIN_LOAN,
        params=params.to_dict(),
    )


@http_factory(loan.AccountBorrowRequest)
def account_repay_http_factory(
    params: loan.AccountBorrowRequest,
):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.MARGIN_REPAY,
        params=params.to_dict(),
    )


@http_factory(loan.MaxBorrowableRequest)
def max_borrowable_http_factory(
    params: loan.MaxBorrowableRequest,
):
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.MARGIN_MAX_BORROWABLE,
        params=params.to_dict(),
    )
