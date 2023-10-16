import dataclasses
from typing import Any, Dict, Generic, List, TypeVar, TypedDict
from enum import Enum

ResponseMessage = Dict | List

Result = TypeVar("Result", dict, list)


class SpotResponseMessage(TypedDict, Generic[Result]):
    id: str
    status: int
    result: Result
