import dataclasses
import time
from typing import Any, Literal

from bittrade_binance_websocket.models import endpoints


@dataclasses.dataclass(frozen=True)
class RequestMessage:
    method: Literal["GET", "POST", "PUT", "DELETE"]
    endpoint: endpoints.BinanceEndpoints
    params: dict[str, Any] = dataclasses.field(default_factory=dict)
    nonce: int = dataclasses.field(default_factory=lambda: int(1e3 * time.time()))
    id: int = 0
