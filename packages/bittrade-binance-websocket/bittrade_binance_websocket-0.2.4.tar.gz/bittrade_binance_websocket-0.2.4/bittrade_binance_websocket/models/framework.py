from dataclasses import dataclass
from typing import Any, Callable, Literal, NamedTuple, Optional

from ccxt import binance
from elm_framework_helpers.ccxt.models.orderbook import Orderbook
from reactivex import Observable
from reactivex.observable import ConnectableObservable
from reactivex.disposable import CompositeDisposable
from reactivex.scheduler import ThreadPoolScheduler
from elm_framework_helpers.websockets import models
from bittrade_binance_websocket.models import UserFeedMessage
from bittrade_binance_websocket.models.loan import (
    AccountBorrowRequest,
    MaxBorrowableRequest,
)
from bittrade_binance_websocket.models.response_message import SpotResponseMessage
from bittrade_binance_websocket.models.rest import margin_account
from bittrade_binance_websocket.models.rest.listen_key import CreateListenKeyResponse
from bittrade_binance_websocket.models.rest.symbol_price_ticker import SymbolPriceTicker
from bittrade_binance_websocket.models.rest.symbol_price_book_ticker import (
    SymbolPriceBookTicker,
)
from bittrade_binance_websocket.models.trade import TradeDataRequest, TradeDict
from bittrade_binance_websocket.models.order import (
    OrderCancelRequest,
    SymbolOrdersCancelRequest,
    PlaceOrderRequest,
    PlaceOrderResponse,
    SymbolOrderResponseItem,
)


class BookConfig(NamedTuple):
    pair: str
    depth: int


@dataclass
class FrameworkContext:
    all_subscriptions: CompositeDisposable
    exchange: binance
    get_active_listen_key_http: Callable[[], Observable[CreateListenKeyResponse]]
    get_account_information_http: Callable[[bool, list[str] | None], Observable[dict]]
    get_listen_key_http: Callable[[], Observable[CreateListenKeyResponse]]
    isolated_margin_get_listen_key_http: Callable[
        [str], Observable[CreateListenKeyResponse]
    ]
    delete_listen_key_http: Callable[[str], Observable[None]]
    keep_alive_listen_key_http: Callable[[str], Observable[None]]
    market_symbol_price_ticker_http: Callable[[str], Observable[SymbolPriceTicker]]
    market_symbol_price_book_ticker_http: Callable[
        [str], Observable[SymbolPriceBookTicker]
    ]
    scheduler: ThreadPoolScheduler
    spot_trade_socket_bundles: ConnectableObservable[models.WebsocketBundle]
    spot_trade_socket_messages: Observable[dict]
    spot_trade_sockets: Observable[models.EnhancedWebsocket]
    spot_trade_guaranteed_sockets: models.EnhancedWebsocketBehaviorSubject
    spot_order_create: Callable[[PlaceOrderRequest], Observable[PlaceOrderResponse]]
    spot_order_cancel: Callable[[OrderCancelRequest], Observable[dict]]
    order_create_http: Callable[[PlaceOrderRequest], Observable[PlaceOrderResponse]]
    order_cancel_http: Callable[[OrderCancelRequest], Observable[dict]]
    order_cancel_http: Callable[[OrderCancelRequest], Observable[dict]]
    trade_list_http: Callable[[TradeDataRequest], Observable[list[TradeDict]]]
    margin_account_borrow_http: Callable[[AccountBorrowRequest], Observable[dict]]
    margin_account_repay_http: Callable[[AccountBorrowRequest], Observable[dict]]
    margin_max_borrowable_http: Callable[[MaxBorrowableRequest], Observable[dict]]
    spot_symbol_orders_cancel: Callable[
        [SymbolOrdersCancelRequest], Observable[SpotResponseMessage]
    ]
    symbol_orders_cancel_http: Callable[
        [SymbolOrdersCancelRequest], Observable[SpotResponseMessage]
    ]
    current_open_orders_http: Callable[
        [SymbolOrdersCancelRequest], Observable[SpotResponseMessage]
    ]
    margin_query_cross_margin_account_details_http: Callable[
        [Optional[bool]], Observable[margin_account.AccountInfo]
    ]
    margin_query_margin_fee_data_http: Callable[
        [str, Optional[bool]], Observable[margin_account.LeverageData]
    ]
    user_data_stream_sockets: Observable[models.EnhancedWebsocket]
    user_data_stream_socket_bundles: ConnectableObservable[models.WebsocketBundle]
    user_data_stream_messages: Observable[UserFeedMessage]
    public_stream_bundles: ConnectableObservable[models.WebsocketBundle]
    public_stream_sockets: Observable[models.EnhancedWebsocket]
    public_stream_socket_messages: Observable[UserFeedMessage]
    isolated_margin_user_stream_factory: Callable[
        [str],
        tuple[
            ConnectableObservable[models.WebsocketBundle],
            Observable[models.EnhancedWebsocket],
            Observable[UserFeedMessage],
        ],
    ]
