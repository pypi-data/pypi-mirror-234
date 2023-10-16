import dataclasses
from datetime import datetime
from logging import getLogger
import time
from typing import Callable, Dict, cast
from uuid import uuid4
from expression import pipe
from reactivex import Observable, compose, operators
from bittrade_binance_websocket.sign import (
    encode_query_string,
    get_signature,
    to_sorted_qs,
)
from bittrade_binance_websocket.events.request_response import (
    response_ok,
    wait_for_response,
)
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket
from bittrade_binance_websocket.models.message import UserFeedMessage
from bittrade_binance_websocket.models.order import (
    OrderCancelRequest,
    SymbolOrdersCancelRequest,
)
from reactivex.disposable import CompositeDisposable
from reactivex.subject import BehaviorSubject
from bittrade_binance_websocket.models.private import PrivateRequest

from bittrade_binance_websocket.models.response_message import (
    ResponseMessage,
    SpotResponseMessage,
)

logger = getLogger(__name__)


@dataclasses.dataclass
class CancelOrderRequest(OrderCancelRequest, PrivateRequest):
    pass


def cancel_order_factory(
    socket: BehaviorSubject[EnhancedWebsocket], messages: Observable[ResponseMessage]
) -> Callable[[OrderCancelRequest], Observable[ResponseMessage]]:
    def cancel_order(request: OrderCancelRequest) -> Observable[ResponseMessage]:
        def subscribe(observer, scheduler):
            sub = CompositeDisposable()
            current_socket = socket.value
            # the helper method will return the request_id but is typed as an int, though here it's a string
            request_id, obs = current_socket.request_to_observable(
                {
                    "method": "order.cancel",
                    "params": request.to_dict(),
                }
            )
            sub.add(
                messages.pipe(
                    wait_for_response(request_id, 5.0),
                    response_ok(),
                ).subscribe(observer, scheduler=scheduler)
            )
            sub.add(obs.subscribe())  # equivalent to sending the request
            return sub

        return Observable(subscribe)

    return cancel_order


def cancel_symbol_orders_factory(
    socket: BehaviorSubject[EnhancedWebsocket],
    messages: Observable[SpotResponseMessage],
) -> Callable[[SymbolOrdersCancelRequest], Observable[SpotResponseMessage]]:
    def cancel_order(
        request: SymbolOrdersCancelRequest,
    ) -> Observable[SpotResponseMessage]:
        def subscribe(observer, scheduler):
            sub = CompositeDisposable()
            current_socket = socket.value
            # the helper method will return the request_id but is typed as an int, though here it's a string
            request_id, obs = current_socket.request_to_observable(
                {
                    "method": "openOrders.cancelAll",
                    "params": request.to_dict(),
                }
            )
            sub.add(
                messages.pipe(
                    wait_for_response(request_id, 5.0),
                    response_ok(),
                ).subscribe(observer, scheduler=scheduler)
            )
            sub.add(obs.subscribe())  # equivalent to sending the request
            return sub

        return Observable(subscribe)

    return cancel_order


def cancel_order(
    messages: Observable[ResponseMessage], request: OrderCancelRequest
) -> Callable[[Observable[EnhancedWebsocket]], Observable[ResponseMessage]]:
    def socket_to_event_messages(
        socket: EnhancedWebsocket,
    ) -> Observable[ResponseMessage]:
        request_id = str(uuid4())
        timestamp = str(int(datetime.now().timestamp() * 1e3))

        # do not allow for both to be None
        if not request.orderId and not request.origClientOrderId:
            raise Exception(
                "cancel order request requires orderId or origClientOrderId to be filled."
            )

        request_dict = request.to_dict()
        request_dict["apiKey"] = socket.key
        request_dict["timestamp"] = timestamp

        order_params = CancelOrderRequest(**request_dict)

        order_request = {
            "id": request_id,
            "method": "order.cancel",
            "params": order_params.to_dict(),
        }
        logger.info(f"cancel order request, {order_request}")

        socket.send_message(order_request)
        return messages.pipe(
            wait_for_response(request_id, 5.0),
            response_ok(),
        )

    return compose(operators.flat_map(socket_to_event_messages))
