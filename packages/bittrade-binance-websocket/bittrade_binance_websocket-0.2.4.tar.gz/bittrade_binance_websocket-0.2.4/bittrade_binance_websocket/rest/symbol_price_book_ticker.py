from typing import TypedDict
from bittrade_binance_websocket.connection import http
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models.rest import symbol_price_book_ticker
import reactivex


def symbol_price_book_ticker_http(
    symbol: str,
) -> reactivex.Observable[symbol_price_book_ticker.SymbolPriceBookTicker]:
    return http.send_request(
        http.prepare_request(
            request.RequestMessage(
                method="GET",
                endpoint=endpoints.BinanceEndpoints.SYMBOL_BOOK_TICKER,
                params={"symbol": symbol},
            )
        )
    )
