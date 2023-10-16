import dataclasses
from enum import Enum
from typing import Optional, TypedDict


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    LIMIT = "LIMIT"
    LIMIT_MAKER = "LIMIT_MAKER"
    MARKET = "MARKET"
    STOP_LOSS = "STOP_LOSS"
    STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"


class OrderTimeInForceType(Enum):
    GTC = "GTC"  # Good 'til Canceled – the order will remain on the book until you cancel it, or the order is completely filled.
    IOC = "IOC"  # Immediate or Cancel – the order will be filled for as much as possible, the unfilled quantity immediately expires.
    FOK = "FOK"  # Fill or Kill – the order will expire unless it cannot be immediately filled for the entire quantity.


class OrderResponseType(Enum):
    ACK = "ACK"
    RESULT = "RESULT"
    FULL = "FULL"


class OrderSelfTradePreventionMode(Enum):
    EXPIRE_TAKER = "EXPIRE_TAKER"
    EXPIRE_MAKER = "EXPIRE_MAKER"
    EXPIRE_BOTH = "EXPIRE_BOTH"
    NONE = "NONE"


class OrderCancelRestrictions(Enum):
    ONLY_NEW = "ONLY_NEW"
    ONLY_PARTIALLY_FILLED = "ONLY_PARTIALLY_FILLED"


"""
Optional without default value is dependant on order type. Set "None" for those that are not related
"""


@dataclasses.dataclass
class PlaceOrderRequest:
    symbol: str
    side: OrderSide
    type: OrderType
    timeInForce: Optional[OrderTimeInForceType]
    price: Optional[str]
    quantity: Optional[str]
    quoteOrderQty: Optional[str]
    stopPrice: Optional[str]
    trailingDelta: Optional[int]
    icebergQty: Optional[str] = None
    strategyId: Optional[int] = None
    strategyType: Optional[int] = None
    selfTradePreventionMode: Optional[OrderSelfTradePreventionMode] = None
    newOrderRespType: Optional[OrderResponseType] = None
    newClientOrderId: Optional[
        str
    ] = None  # Arbitrary unique ID among open orders. Automatically generated if not sent
    recvWindow: Optional[int] = None
    is_margin: Optional[bool] = False
    isIsolated: Optional[bool] = None

    def to_dict(self):
        as_dict = dataclasses.asdict(self)
        del as_dict["is_margin"]
        if self.is_margin:
            as_dict["isIsolated"] = "TRUE" if self.isIsolated else "FALSE"
        else:
            del as_dict["isIsolated"]
        for key in (
            "newOrderRespType",
            "selfTradePreventionMode",
            "side",
            "type",
            "timeInForce",
        ):
            if enum_value := getattr(self, key, None):
                as_dict[key] = enum_value.value
        return as_dict


@dataclasses.dataclass
class PlaceOrderResponse:
    symbol: str
    orderId: int
    orderListId: int
    clientOrderId: str
    transactTime: int


class SymbolOrderResponseItem(TypedDict):
    symbol: str
    origClientOrderId: str
    orderId: int
    orderListId: int
    clientOrderId: str
    price: str
    origQty: str
    executedQty: str
    cummulativeQuoteQty: str
    status: str
    timeInForce: str
    type: str
    side: str
    selfTradePreventionMode: str


@dataclasses.dataclass
class OrderCancelRequest:
    symbol: str
    origClientOrderId: Optional[str]
    orderId: Optional[int]
    newClientOrderId: Optional[str] = None
    cancelRestrictions: Optional[OrderCancelRestrictions] = None
    recvWindow: Optional[int] = None
    is_margin: Optional[bool] = False
    isIsolated: Optional[bool] = None

    def to_dict(self):
        as_dict = dataclasses.asdict(self)
        del as_dict["is_margin"]
        if self.is_margin:
            as_dict["isIsolated"] = "TRUE" if self.isIsolated else "FALSE"
        else:
            del as_dict["isIsolated"]
        return as_dict


@dataclasses.dataclass
class SymbolOrdersCancelRequest:
    symbol: str
    recvWindow: Optional[int] = None
    is_margin: Optional[bool] = False
    isIsolated: Optional[bool] = None

    def to_dict(self):
        as_dict = dataclasses.asdict(self)
        del as_dict["is_margin"]
        if self.is_margin:
            as_dict["isIsolated"] = "TRUE" if self.isIsolated else "FALSE"
        else:
            del as_dict["isIsolated"]
        return as_dict


class UserDataStreamOrder(TypedDict):
    E: int  # Event time
    s: str  # Symbol
    c: str  # Client order ID
    S: str  # Side
    o: str  # Order type
    f: str  # Time in force
    q: str  # Order quantity
    p: str  # Order price
    P: str  # Stop price
    d: int  # Trailing Delta
    F: str  # Iceberg quantity
    g: int  # OrderListId
    C: str  # Original client order ID
    x: str  # Current execution type
    X: str  # Current order status
    r: str  # Order reject reason
    i: int  # Order ID
    l: str  # Last executed quantity
    z: str  # Cumulative filled quantity
    L: str  # Last executed price
    n: str  # Commission amount
    N: str | None  # Commission asset
    T: int  # Transaction time
    t: int  # Trade ID
    v: int  # Prevented Match Id
    I: int  # Ignore
    w: bool  # Is the order on the book?
    m: bool  # Is this trade the maker side?
    M: bool  # Ignore
    O: int  # Order creation time
    Z: str  # Cumulative quote asset transacted quantity
    Y: str  # Last quote asset transacted quantity
    Q: str  # Quote Order Quantity
    D: int  # Trailing Time
    j: int  # Strategy ID
    J: int  # Strategy Type
    W: int  # Working Time
    V: str  # Self-trade prevention mode
    u: int  # TradeGroupId
    U: int  # CounterOrderId
    A: str  # Prevented Quantity
    B: str  # Last Prevented Quantity
