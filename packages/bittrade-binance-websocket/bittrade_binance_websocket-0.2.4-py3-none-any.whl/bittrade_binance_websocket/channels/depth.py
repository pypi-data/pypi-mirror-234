from typing import Any, Callable, Dict, List, cast
from reactivex import Observable, compose, operators
from ccxt import binance
from bittrade_binance_websocket.channels.subscribe import subscribe_to_channel

from bittrade_binance_websocket.models import response_message
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket
from bittrade_binance_websocket.models.message import UserFeedMessage

def extract_data():
    def _extract(message: UserFeedMessage):
      return message

    return _extract

def parse_order_book_ccxt(exchange: binance):
   def _parse_order_book_ccxt(messages: UserFeedMessage):
      timestamp = messages.get('E', '')
      symbol = messages.get('s', '')
      return exchange.parse_order_book(messages, symbol, timestamp, bidsKey='b', asksKey='a')
   
   return _parse_order_book_ccxt

def subscribe_depth(
    messages: Observable[Dict | List],
    symbol: str,
    depth_level: int = 5,
    update_speed: int = 100
) -> Callable[[Observable[EnhancedWebsocket]], Observable[UserFeedMessage]]:
    """Unparsed orders (only extracted result array)"""
    ticker = f'{symbol}@depth'
    return compose(
        subscribe_to_channel(messages, ticker),
        operators.map(extract_data()),
    )


__all__ = ["subscribe_depth", "parse_order_book_ccxt"]