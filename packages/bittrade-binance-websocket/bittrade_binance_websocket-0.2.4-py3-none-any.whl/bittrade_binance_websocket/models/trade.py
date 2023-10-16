from dataclasses import dataclass
import dataclasses
from datetime import datetime
from typing import Optional, TypedDict

@dataclass
class TradeDataRequest:
    symbol: str
    orderId: Optional[int] = None
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    fromId: Optional[int] = None
    limit: int = 1000
    is_margin: bool = False
    isIsolated: Optional[bool] = None

    def to_dict(self):
        as_dict = dataclasses.asdict(self)
        del as_dict["is_margin"]
        if self.is_margin:
            as_dict["isIsolated"] = "TRUE" if self.isIsolated else "FALSE"
        else:
            del as_dict["isIsolated"]
        for k in ["startTime", "endTime"]:
            v: datetime
            if v := getattr(self, k, None):
                as_dict[k] = int(v.timestamp() * 1e3)
        return as_dict
    
class TradeDict(TypedDict):
    symbol: str
    id: int
    orderId: int
    orderListId: int
    price: str
    qty: str
    quoteQty: str
    commission: str
    commissionAsset: str
    time: int
    isBuyer: bool
    isMaker: bool
    isBestMatch: bool