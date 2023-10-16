from typing import Dict, List, Tuple, TypedDict, Literal


class PrivateSequence(TypedDict):
    sequence: int


PrivateMessage = PrivateSequence

# Note that these don't match quite Orderbook update messages which may have 5 values
PublicMessage = Dict

UserFeedMessage = PrivateMessage | PublicMessage


class UserDataStreamMessage(TypedDict):
    e: Literal["outboundAccountInfo", "executionReport", "outboundAccountPosition"]
