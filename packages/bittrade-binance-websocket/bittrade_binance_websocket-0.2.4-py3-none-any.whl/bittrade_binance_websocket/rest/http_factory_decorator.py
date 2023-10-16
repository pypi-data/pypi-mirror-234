import functools
from typing import Any, Callable, ParamSpec, Type, TypeVar, TypedDict, cast
import requests
from bittrade_binance_websocket import models
from bittrade_binance_websocket.connection import http
from reactivex import Observable

P = ParamSpec("P")


# TODO this typing does not work, it does not allow us to define the sub type of the response's result
R = TypeVar("R")


def http_factory(return_type: Type):
    def factory_wrapper(
        fn: Callable[P, models.RequestMessage]
    ) -> Callable[
        [Callable[[requests.models.Request], requests.models.Request]],
        Callable[P, Observable[return_type]],
    ]:
        @functools.wraps(fn)
        def factory(
            add_token: Callable[[requests.models.Request], requests.models.Request]
        ):
            def inner(*args: P.args, **kwargs: P.kwargs) -> Observable[return_type]:
                request = fn(*args, **kwargs)
                return cast(
                    Observable[return_type],
                    http.send_request(add_token(http.prepare_request(request))),
                )

            return inner

        return factory

    return factory_wrapper
