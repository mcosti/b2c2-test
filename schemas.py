from dataclasses import dataclass
from datetime import datetime

import dateutil.parser
from dateutil.tz import tzutc
from typing import List


@dataclass
class Quote:
    valid_until: datetime
    rfq_id: str
    client_rfq_id: str
    quantity: float
    side: str
    instrument: str
    price: float
    created: datetime
    
    def __post_init__(self):
        self.valid_until = dateutil.parser.isoparse(self.valid_until)
        self.created = dateutil.parser.isoparse(self.created)
        self.quantity = float(self.quantity)
        self.price = float(self.price)

    @property
    def is_expired(self):
        return datetime.now(tzutc()) > self.valid_until


@dataclass
class Order:
    order_id: str
    client_order_id: str
    quantity: float
    side: str
    instrument: str
    price: float
    executing_unit: str
    trades: List[dict]
    created: datetime
    executed_price: float = None

    def __post_init__(self):
        self.created = dateutil.parser.isoparse(self.created)
        self.quantity = float(self.quantity)
        self.price = float(self.price)
        self.executed_price = float(self.executed_price) if self.executed_price else None

    @property
    def is_rejected(self):
        return self.executed_price is None
