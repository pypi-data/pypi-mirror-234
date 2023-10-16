import dataclasses
from datetime import datetime
from typing import Callable
from bittrade_binance_websocket.connection import http
from bittrade_binance_websocket.models import endpoints, trade, request
import requests
from reactivex import Observable, operators
from reactivex.abc import ObserverBase, SchedulerBase
import reactivex

def _account_trade_list_process(params: trade.TradeDataRequest, load: Callable[[trade.TradeDataRequest], Observable[list[trade.TradeDict]]]):
    """TODO this is the testable version - let's write tests for it"""
    current_params = dataclasses.replace(params)
    last_id = 0
    def local_load(_):
        return load(current_params)

    def emit_data(data: list[trade.TradeDict]):
        nonlocal last_id
        has_next_page = len(data) == params.limit
        # After first page, and if we have more data, the first item in next data will be the last item in previous data, so we should remove that value
        if last_id and last_id == data[0]["id"]:
            data = data[1:]
        ret = reactivex.just(data)
        if has_next_page:
            current_params.startTime = None
            last_id = data[-1]["id"]
            current_params.fromId = last_id
            ret = reactivex.concat(ret, reactivex.throw(Exception("More data available")))
        return ret
    return reactivex.defer(local_load).pipe(
        operators.flat_map(emit_data),
        operators.retry()
    )
    
    

def account_trade_list_http_factory(
    add_token: Callable[[requests.models.Request], requests.models.Request]
):
    def _account_trade_list_http(params: trade.TradeDataRequest):
        def load(p: trade.TradeDataRequest):
            r = request.RequestMessage(
                method="GET",
                endpoint=endpoints.BinanceEndpoints.MARGIN_TRADE_LIST if params.is_margin else endpoints.BinanceEndpoints.SPOT_TRADE_LIST,
                params=p.to_dict(),
            )
            return http.send_request(add_token(http.prepare_request(r)))
        # Simple case where we want to load just the most recent data
        if not params.startTime and not params.fromId:
            return load(params)
        return _account_trade_list_process(params, load)

        
    return _account_trade_list_http


