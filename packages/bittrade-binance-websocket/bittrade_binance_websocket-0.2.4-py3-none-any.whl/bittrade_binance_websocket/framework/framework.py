from logging import getLogger
from typing import Callable, cast

import requests
from ccxt import binance
from elm_framework_helpers.websockets.operators import connection_operators
from reactivex import Observable, operators
from reactivex.disposable import CompositeDisposable
from reactivex.scheduler import ThreadPoolScheduler
from reactivex.subject import BehaviorSubject

from bittrade_binance_websocket import models
from bittrade_binance_websocket.connection.public_stream import (
    public_websocket_connection,
)
from bittrade_binance_websocket.connection.private import private_websocket_connection
from bittrade_binance_websocket.connection.private_user_stream import (
    private_websocket_user_stream,
)
from bittrade_binance_websocket.events.add_order import create_order_factory
from bittrade_binance_websocket.events.cancel_order import (
    cancel_order_factory,
    cancel_symbol_orders_factory,
)
from bittrade_binance_websocket.rest.account_information import (
    get_account_information_http_factory,
)
from bittrade_binance_websocket.rest.cancel_order import cancel_order_http_factory
from bittrade_binance_websocket.rest.query_margin_account import (
    query_margin_account_details_http_factory,
)
from bittrade_binance_websocket.rest.trade_list import account_trade_list_http_factory
from bittrade_binance_websocket.rest.query_margin_fee_data import (
    query_margin_fee_data_http_factory,
)
from bittrade_binance_websocket.rest.symbol_orders_cancel import (
    delete_symbol_order_http_factory,
)
from bittrade_binance_websocket.rest.create_order import (
    create_order_http_factory,
)
from bittrade_binance_websocket.rest.current_open_orders import (
    open_orders_http_factory,
)
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket
from bittrade_binance_websocket.models.framework import FrameworkContext
from bittrade_binance_websocket.rest.symbol_price_ticker import symbol_price_ticker_http
from bittrade_binance_websocket.rest.symbol_price_book_ticker import (
    symbol_price_book_ticker_http,
)
from bittrade_binance_websocket.rest.listen_key import (
    delete_listen_key_http_factory,
    get_active_listen_key_http_factory,
    get_listen_key_http_factory,
    isolated_margin_delete_listen_key_http_factory,
    isolated_margin_get_active_listen_key_http_factory,
    isolated_margin_get_listen_key_http_factory,
    isolated_margin_ping_listen_key_http_factory,
    ping_listen_key_http_factory,
)
from bittrade_binance_websocket.rest.margin_loan import (
    account_borrow_http_factory,
    account_repay_http_factory,
    max_borrowable_http_factory,
)

logger = getLogger(__name__)


def get_framework(
    *,
    user_stream_signer_http: Callable[
        [requests.models.Request], requests.models.Request
    ] = None,  # type: ignore
    spot_trade_signer: Callable[
        [models.EnhancedWebsocket], models.EnhancedWebsocket
    ] = None,  # type: ignore
    trade_signer_http: Callable[
        [requests.models.Request], requests.models.Request
    ] = None,  # type: ignore
    load_markets=True,
) -> FrameworkContext:
    exchange = binance()
    if load_markets:
        exchange.load_markets()
    pool_scheduler = ThreadPoolScheduler(200)
    all_subscriptions = CompositeDisposable()
    # Rest
    get_active_listen_key_http = get_active_listen_key_http_factory(
        user_stream_signer_http
    )
    get_account_information_http = get_account_information_http_factory(
        trade_signer_http
    )
    get_listen_key_http = get_listen_key_http_factory(user_stream_signer_http)
    keep_alive_listen_key_http = ping_listen_key_http_factory(user_stream_signer_http)
    delete_listen_key_http = delete_listen_key_http_factory(user_stream_signer_http)
    isolated_margin_get_listen_key_http = (
        isolated_margin_get_active_listen_key_http_factory(user_stream_signer_http)
    )
    isolated_margin_keep_alive_listen_key_http = (
        isolated_margin_ping_listen_key_http_factory(user_stream_signer_http)
    )
    isolated_margin_delete_listen_key_http = (
        isolated_margin_delete_listen_key_http_factory(user_stream_signer_http)
    )

    # Setup up public stream
    public_stream_bundles = public_websocket_connection()
    public_stream_sockets = public_stream_bundles.pipe(
        connection_operators.keep_new_socket_only(),
        operators.share(),
    )
    public_stream_socket_messages = public_stream_bundles.pipe(
        connection_operators.keep_messages_only(), operators.share()
    )

    # Set up sockets
    user_data_stream_socket_bundles = private_websocket_user_stream(
        get_listen_key_http, keep_alive_listen_key_http
    )
    user_data_stream_socket = user_data_stream_socket_bundles.pipe(
        connection_operators.keep_new_socket_only()
    )

    user_data_stream_messages = user_data_stream_socket_bundles.pipe(
        connection_operators.keep_messages_only()
    )

    def isolated_margin_user_stream_factory(symbol: str):
        key_getter = lambda: isolated_margin_get_listen_key_http(symbol)
        keep_alive = lambda key: isolated_margin_keep_alive_listen_key_http(key, symbol)
        socket_bundles = private_websocket_user_stream(key_getter, keep_alive)
        socket = socket_bundles.pipe(connection_operators.keep_new_socket_only())

        stream_messages = socket_bundles.pipe(connection_operators.keep_messages_only())
        return socket_bundles, socket, stream_messages

    spot_trade_socket_bundles = private_websocket_connection()
    spot_trade_sockets = spot_trade_socket_bundles.pipe(
        connection_operators.keep_new_socket_only(),
        operators.map(spot_trade_signer),  # add authentication details
        operators.share(),
    )
    spot_trade_guaranteed_sockets: BehaviorSubject[EnhancedWebsocket] = BehaviorSubject(
        cast(EnhancedWebsocket, None)
    )
    spot_trade_sockets.subscribe(spot_trade_guaranteed_sockets)
    spot_trade_socket_messages = spot_trade_socket_bundles.pipe(
        connection_operators.keep_messages_only(), operators.share()
    )
    spot_order_create = create_order_factory(
        spot_trade_guaranteed_sockets, spot_trade_socket_messages
    )
    spot_order_cancel = cancel_order_factory(
        spot_trade_guaranteed_sockets, spot_trade_socket_messages
    )
    spot_symbol_orders_cancel = cancel_symbol_orders_factory(
        spot_trade_guaranteed_sockets, spot_trade_socket_messages
    )
    symbol_orders_cancel_http = delete_symbol_order_http_factory(trade_signer_http)
    open_orders_http = open_orders_http_factory(trade_signer_http)
    query_cross_margin_account_details_http = query_margin_account_details_http_factory(
        trade_signer_http
    )
    query_margin_fee_data_http = query_margin_fee_data_http_factory(trade_signer_http)

    return FrameworkContext(
        all_subscriptions=all_subscriptions,
        exchange=exchange,
        delete_listen_key_http=delete_listen_key_http,
        get_account_information_http=get_account_information_http,
        get_active_listen_key_http=get_active_listen_key_http,
        get_listen_key_http=get_listen_key_http,
        isolated_margin_get_listen_key_http=isolated_margin_get_listen_key_http,
        isolated_margin_user_stream_factory=isolated_margin_user_stream_factory,
        keep_alive_listen_key_http=keep_alive_listen_key_http,
        market_symbol_price_ticker_http=symbol_price_ticker_http,
        market_symbol_price_book_ticker_http=symbol_price_book_ticker_http,
        margin_query_cross_margin_account_details_http=query_cross_margin_account_details_http,
        margin_query_margin_fee_data_http=query_margin_fee_data_http,
        margin_account_borrow_http=account_borrow_http_factory(trade_signer_http),
        margin_account_repay_http=account_repay_http_factory(trade_signer_http),
        margin_max_borrowable_http=max_borrowable_http_factory(trade_signer_http),
        spot_trade_socket_bundles=spot_trade_socket_bundles,
        spot_trade_socket_messages=spot_trade_socket_messages,
        spot_trade_sockets=spot_trade_sockets,
        spot_trade_guaranteed_sockets=spot_trade_guaranteed_sockets,
        spot_order_create=spot_order_create,
        spot_order_cancel=spot_order_cancel,
        spot_symbol_orders_cancel=spot_symbol_orders_cancel,
        order_create_http=create_order_http_factory(trade_signer_http),
        order_cancel_http=cancel_order_http_factory(trade_signer_http),
        trade_list_http=account_trade_list_http_factory(trade_signer_http),
        symbol_orders_cancel_http=symbol_orders_cancel_http,
        current_open_orders_http=open_orders_http,
        user_data_stream_messages=user_data_stream_messages,
        user_data_stream_sockets=user_data_stream_socket,
        user_data_stream_socket_bundles=user_data_stream_socket_bundles,
        public_stream_bundles=public_stream_bundles,
        public_stream_sockets=public_stream_sockets,
        public_stream_socket_messages=public_stream_socket_messages,
        scheduler=pool_scheduler,
    )
