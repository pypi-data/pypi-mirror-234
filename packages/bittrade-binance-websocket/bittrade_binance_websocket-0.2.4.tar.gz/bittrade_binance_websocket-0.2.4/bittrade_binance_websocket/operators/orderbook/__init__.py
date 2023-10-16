from typing import Callable, Any
from reactivex import operators, Observable


def map_bids_only() -> Callable[[Observable[dict]], Observable[list[tuple[float, ...]]]]:
    return operators.map(lambda x: x["bids"])


def map_asks_only() -> Callable[[Observable[dict]], Observable[list[tuple[float, ...]]]]:
    return operators.map(lambda x: x["asks"])

def _best_price(x: list[tuple[float, ...]]):
    return x[0][0]

def map_top_prices() -> Callable[[Observable[Any]], Observable[tuple[float, float]]]:
    return operators.map(lambda x: (_best_price(x["bids"]), _best_price(x["asks"])))

def map_best_price() -> Callable[[Observable[list[tuple[float, ...]]]], Observable[float]]:
    return operators.map(_best_price)
