from bittrade_binance_websocket.connection import http
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models.rest import get_time
import reactivex


def get_time_http() -> reactivex.Observable[get_time.GetTimeResponse]:
    return http.send_request(
        http.prepare_request(
            request.RequestMessage(
                method="GET",
                endpoint=endpoints.BinanceEndpoints.GET_TIME,
            )
        )
    )
