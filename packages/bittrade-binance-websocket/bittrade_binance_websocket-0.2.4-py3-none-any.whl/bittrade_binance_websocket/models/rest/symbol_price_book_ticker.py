from typing import TypedDict


class SymbolPriceBookTicker(TypedDict):
    symbol: str
    bidPrice: str
    bidQty: str
    askPrice: str
    askQty: str
