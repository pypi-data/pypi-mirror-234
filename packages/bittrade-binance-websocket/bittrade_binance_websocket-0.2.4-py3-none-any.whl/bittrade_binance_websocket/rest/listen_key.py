from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models.rest import listen_key

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(listen_key.CreateListenKeyResponse)
def get_listen_key_http_factory():
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
    )


@http_factory(None)
def ping_listen_key_http_factory(listen_key: str):
    return request.RequestMessage(
        method="PUT",
        endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
        params={
            "listenKey": listen_key,
        },
    )


@http_factory(listen_key.CreateListenKeyResponse)
def get_active_listen_key_http_factory():
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
    )


@http_factory(None)
def delete_listen_key_http_factory(listen_key: str):
    return request.RequestMessage(
        method="DELETE",
        endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
        params={
            "listenKey": listen_key,
        },
    )


@http_factory(listen_key.CreateListenKeyResponse)
def isolated_margin_get_listen_key_http_factory(symbol: str):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.ISOLATED_MARGIN_LISTEN_KEY,
        params={
            "symbol": symbol,
        },
    )


@http_factory(None)
def isolated_margin_ping_listen_key_http_factory(listen_key: str, symbol: str):
    return request.RequestMessage(
        method="PUT",
        endpoint=endpoints.BinanceEndpoints.ISOLATED_MARGIN_LISTEN_KEY,
        params={
            "listenKey": listen_key,
            "symbol": symbol,
        },
    )


@http_factory(listen_key.CreateListenKeyResponse)
def isolated_margin_get_active_listen_key_http_factory(symbol: str):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.ISOLATED_MARGIN_LISTEN_KEY,
        params={
            "symbol": symbol,
        },
    )


@http_factory(None)
def isolated_margin_delete_listen_key_http_factory(listen_key: str, symbol: str):
    return request.RequestMessage(
        method="DELETE",
        endpoint=endpoints.BinanceEndpoints.ISOLATED_MARGIN_LISTEN_KEY,
        params={
            "listenKey": listen_key,
            "symbol": symbol,
        },
    )
