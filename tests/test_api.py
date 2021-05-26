"""Only some minimal testing"""
from datetime import datetime, timedelta
from unittest import mock

import pytest
from dateutil.tz import tzutc

from api import b2c2_api as api
from exceptions import QuoteExpiredException, OrderRejectedException
from schemas import Quote
from tests.dummy_data import (
    dummy_quote_response,
    dummy_order_rejected_response,
    dummy_order_response,
    dummy_instruments_response
)


@pytest.fixture
def quote():
    return Quote(**dummy_quote_response)


def test_create_order_with_expired_quote(quote):
    quote.valid_until = datetime.now(tzutc()) - timedelta(minutes=10)

    with pytest.raises(QuoteExpiredException):
        api.create_order(quote)


def test_create_order_rejected(quote):
    with mock.patch('api.B2C2Api.request', return_value=dummy_order_rejected_response):
        with pytest.raises(OrderRejectedException):
            api.create_order(quote)


def test_create_order_success(quote):
    with mock.patch('api.B2C2Api.request', return_value=dummy_order_response):
        order = api.create_order(quote)
        assert order.executed_price == 10457.651100000


def test_get_instruments():
    with mock.patch('api.B2C2Api.request', return_value=dummy_instruments_response):
        instruments = api.get_instruments()
        assert instruments == ["BTCUSD.CFD", "BTCUSD.SPOT", "BTCEUR.SPOT"]
