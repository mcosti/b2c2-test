from datetime import datetime
from dateutil.tz import tzutc

from schemas import Quote, Order
from tests.dummy_data import dummy_quote_response, dummy_order_response, dummy_order_rejected_response


def test_quote_response():
    quote = Quote(**dummy_quote_response)
    assert quote.valid_until == datetime(2027, 1, 1, 19, 45, 22, 25464, tzinfo=tzutc())
    assert quote.quantity == 1.23
    assert quote.price == 700.0


def test_order_response():
    order = Order(**dummy_order_response)
    assert not order.is_rejected


def test_order_rejected_response():
    order = Order(**dummy_order_rejected_response)
    assert order.is_rejected
