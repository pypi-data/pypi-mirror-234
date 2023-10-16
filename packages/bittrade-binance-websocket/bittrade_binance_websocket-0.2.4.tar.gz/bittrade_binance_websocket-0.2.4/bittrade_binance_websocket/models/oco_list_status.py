from enum import Enum


class BinanceOCOListStatus(Enum):
    RESPONSE = 'RESPONSE'	# This is used when the ListStatus is responding to a failed action. (E.g. Orderlist placement or cancellation)
    EXEC_STARTED = 'EXEC_STARTED'	# The order list has been placed or there is an update to the order list status.
    ALL_DONE = 'ALL_DONE'	# The order list has finished executing and thus no longer active.
