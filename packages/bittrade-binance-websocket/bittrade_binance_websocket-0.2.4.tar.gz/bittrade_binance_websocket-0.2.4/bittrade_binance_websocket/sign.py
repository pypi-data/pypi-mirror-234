from enum import Enum
import hashlib
import hmac
from typing import Any, Dict, Tuple, Union, cast
from urllib.parse import urlencode

from expression import curry_flip
from datetime import datetime

import requests


def del_none(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d


def to_sorted_qs(values: Union[Dict[str, Any], Any]) -> Tuple[Tuple[str, Any]]:
    """
    Returns a tuple of sorted key-value pairs from the given dictionary.

    Args:
    - values: A dictionary containing key-value pairs.

    Returns:
    - A tuple of sorted key-value pairs, where each pair is represented as a tuple of two elements,
    the first being the key and the second being the corresponding value.
    """
    sorted_tuple = tuple()
    keys = sorted(values)
    for key in keys:
        value = values[key]
        if isinstance(value, Enum):
            value = cast(Enum, value).value

        # remove None
        if value is not None:
            sorted_tuple = sorted_tuple + (
                (
                    key,
                    value,
                ),
            )

    return sorted_tuple


def encode_query_string(params: Tuple):
    """
    Returns the URL-encoded string representation of the given tuple of key-value pairs.

    Args:
    - params: A tuple of key-value pairs.

    Returns:
    - The URL-encoded string representation of the given tuple of key-value pairs.
    """
    encoded = urlencode(params)
    return encoded


@curry_flip(1)
def get_signature(qs: str, secret: str):
    """
    Returns the SHA-256 HMAC signature of the given query string using the provided secret key.

    Args:
    - qs: The query string to sign.
    - secret: The secret key to use for signing.

    Returns:
    - The SHA-256 HMAC signature of the given query string using the provided secret key.
    """
    signed = hmac.new(secret.encode("utf-8"), qs.encode("utf-8"), hashlib.sha256)
    return signed.hexdigest()


def sign_request_factory(key: str, secret: str):
    print(
        "Sign request factory is provided for reference only; you should probably copy or rewrite this function for security."
    )

    def hashing(query_string):
        return hmac.new(
            secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def sign(request: requests.models.Request) -> requests.models.Request:
        request.headers.update({"X-MBX-APIKEY": key})
        if request.method == "GET":
            payload = request.params
        else:
            payload = request.data
        payload = del_none(payload)
        # Code adapted from https://github.com/binance/binance-signature-examples/blob/master/python/spot/spot.py
        query_string = urlencode(payload, True)
        ts = int(datetime.now().timestamp() * 1000)
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, ts)
        else:
            query_string = "timestamp={}".format(ts)

        url = request.url + "?" + query_string + "&signature=" + hashing(query_string)
        request.data = {}
        request.params = {}
        request.url = url
        return request

    return sign


def user_stream_signer_factory(key: str):
    """
    Use this for endpoints that require the USER_STREAM type of security.
    Refer to https://binance-docs.github.io/apidocs/spot/en/#endpoint-security-type
    """

    def _add_api_key(request: requests.models.Request):
        request.headers.update({"X-MBX-APIKEY": key})
        return request

    return _add_api_key
