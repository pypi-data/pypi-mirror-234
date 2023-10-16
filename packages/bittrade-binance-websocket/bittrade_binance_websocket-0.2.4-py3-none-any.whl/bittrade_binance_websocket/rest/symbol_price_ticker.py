from typing import TypedDict
from bittrade_binance_websocket.connection import http
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models.rest import symbol_price_ticker
import reactivex


def symbol_price_ticker_http(
    symbol: str,
) -> reactivex.Observable[symbol_price_ticker.SymbolPriceTicker]:
    return http.send_request(
        http.prepare_request(
            request.RequestMessage(
                method="GET",
                endpoint=endpoints.BinanceEndpoints.SYMBOL_PRICE_TICKER,
                params={"symbol": symbol},
            )
        )
    )
