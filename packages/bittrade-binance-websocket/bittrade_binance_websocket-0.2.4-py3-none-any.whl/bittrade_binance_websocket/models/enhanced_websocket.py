from datetime import datetime
from typing import Any, Callable, Optional
from uuid import uuid4
from elm_framework_helpers.websockets import models
import orjson
from bittrade_binance_websocket.sign import (
    del_none,
    encode_query_string,
    get_signature,
    to_sorted_qs,
)
from expression.core import pipe


class EnhancedWebsocket(models.EnhancedWebsocket):
    key: Optional[str] = None
    secret: Optional[str] = None

    def get_timestamp(self) -> str:
        return str(int(datetime.now().timestamp() * 1e3))

    def send_message(self, message: Any) -> int | str:
        return self.send_json(message)

    def prepare_request(self, original_message: dict) -> tuple[str | int, bytes]:
        self._id = self._id + 1
        message = original_message.copy()

        if self.secret:
            # means is private request
            signer, get_timestamp = get_signature(self.secret), self.get_timestamp
            id = message.get("id", str(uuid4()))
            message["id"] = id
            params = pipe(
                message.get("params", {}).copy(), del_none,
                lambda x: {**x, "apiKey": self.key, "timestamp": get_timestamp()},
                lambda x: {
                    **x,
                    "signature": pipe(x, to_sorted_qs, encode_query_string, signer),
                }
            )
            message["params"] = params
            # TODO accept a function to sign the request rather than hardcoding the credentials
        
        message["id"] = message.get("id", self._id)
        return message["id"], orjson.dumps(message)
