from enum import Enum


class TradeAccountType(Enum):
    SPOT = "SPOT"
    MARGIN = "MARGIN"
    FUTURES = "FUTURES"
    ISOLATED_MARGIN = "ISOLATED_MARGIN"
    ISOLATED_FUTURES = "ISOLATED_FUTURES"
