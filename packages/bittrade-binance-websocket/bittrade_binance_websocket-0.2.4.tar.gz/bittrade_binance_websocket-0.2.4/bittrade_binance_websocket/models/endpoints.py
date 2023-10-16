from enum import Enum


# https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md
class BinanceEndpoints(Enum):
    SPOT_OPEN_ORDERS = "/api/v3/openOrders"
    ACCOUNT_INFORMATION = "/api/v3/account"
    GET_TIME = "/api/v3/time"
    ISOLATED_MARGIN_LISTEN_KEY = "/sapi/v1/userDataStream/isolated"
    LISTEN_KEY = "/api/v3/userDataStream"
    MARGIN_OPEN_ORDERS = "/sapi/v1/margin/openOrders"
    MARGIN_ORDER = "/sapi/v1/margin/order"
    MARGIN_MAX_BORROWABLE = "/sapi/v1/margin/maxBorrowable"
    MARGIN_ACCOUNT_INFORMATION = "/sapi/v1/margin/isolated/account"
    MARGIN_LOAN = "/sapi/v1/margin/loan"
    MARGIN_REPAY = "/sapi/v1/margin/repay"
    SPOT_ORDER = "/api/v3/order"
    SPOT_TRADE_LIST = "/api/v3/myTrades"
    MARGIN_TRADE_LIST = "/sapi/v1/margin/myTrades"
    QUERY_CROSS_MARGIN_ACCOUNT_DETAILS = "/sapi/v1/margin/account"
    QUERY_ISOLATED_MARGIN_ACCOUNT_DETAILS = "/sapi/v1/margin/isolated/account"
    QUERY_ISOLATED_MARGIN_FEE_DATA = "/sapi/v1/margin/isolatedMarginData"
    QUERY_CROSS_MARGIN_FEE_DATA = "/sapi/v1/margin/crossMarginData"
    SYMBOL_PRICE_TICKER = "/api/v3/ticker/price"
    SYMBOL_BOOK_TICKER = "/api/v3/ticker/bookTicker"
