# @bookTicker
from typing import Any, Callable, Dict, List, cast
from reactivex import Observable, compose, operators
from ccxt import binance
from bittrade_binance_websocket.channels.subscribe import subscribe_to_channel

from bittrade_binance_websocket.models import response_message
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket
from bittrade_binance_websocket.models.message import UserFeedMessage

# TODO://
def extract_data():
    def _extract(message: UserFeedMessage):
      return message

    return _extract

# TODO: investigate which is the right method to parse to ccxt
def parse_book_ticker_ccxt(exchange: binance):
   def _parse_book_ticker_ccxt(messages: UserFeedMessage):
      symbol = messages.get('s', '')
      market = exchange.market(symbol)
      # not really the same
      return exchange.parse_ticker(messages, market)
   
   return _parse_book_ticker_ccxt

def subscribe_book_ticker(
    messages: Observable[Dict | List],
    symbol: str
) -> Callable[[Observable[EnhancedWebsocket]], Observable[UserFeedMessage]]:
    """Unparsed orders (only extracted result array)"""
    ticker = f'{symbol}@bookTicker'
    return compose(
        subscribe_to_channel(messages, ticker),
        operators.map(extract_data()),
    )


__all__ = ["subscribe_book_ticker", "parse_book_ticker_ccxt"]