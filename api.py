import logging
import os
import uuid

import requests
from furl import furl

import exceptions
from schemas import Quote, Order

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ORDER_TYPE = 'FOK'
EXECUTING_UNIT = 'risk-adding-strategy'


def handle_errors(data):
    if isinstance(data, list):
        return

    errors = data.get('errors', [])
    if not errors:
        return

    # I am gonna treat just the first error

    [error] = errors
    error_message = error.get('message')
    error_code = error.get('code')

    if error_code == 1012:
        raise exceptions.RiskExposureTooHighException(error_message)

    if error_code == 1010:
        raise exceptions.MaximumQuantityExceededException(error_message)


class B2C2Api:
    endpoint = "https://api.uat.b2c2.net/"
    # endpoint = "https://b2c2-test.free.beeceptor.com"  # Mock I used for testing

    def __init__(self):
        token = os.getenv("B2C2_TOKEN", "e13e627c49705f83cbe7b60389ac411b6f86fee7")
        self.headers = {"Authorization": f"Token {token}"}

    def request(self, method, path, payload=None):
        path = furl(self.endpoint).add(path=path + '/')
        logger.info(f"Requesting {method} {path} \n")
        response = requests.request(method, path, headers=self.headers, json=payload)
        data = response.json()

        handle_errors(data)
        response.raise_for_status()
        return data

    def request_quote(self, instrument: str, side: str, quantity: float) -> Quote:
        payload = {
            'instrument': instrument,
            'side': side.lower(),
            'quantity': str(quantity),
            'client_rfq_id': str(uuid.uuid4())
        }
        response_json = self.request('POST', 'request_for_quote', payload)
        return Quote(**response_json)

    def create_order(self, quote: Quote):
        if quote.is_expired:
            raise exceptions.QuoteExpiredException

        payload = {
            'instrument': quote.instrument,
            'side': quote.side.lower(),
            'quantity': str(quote.quantity),
            'client_order_id': quote.client_rfq_id,
            'price': str(quote.price),
            'order_type': ORDER_TYPE,
            'valid_until': quote.valid_until.strftime("%Y-%m-%dT%H:%M:%S"),
            'executing_unit': EXECUTING_UNIT,
        }

        response_json = self.request('POST', 'order', payload)
        order = Order(**response_json)

        if order.is_rejected:
            raise exceptions.OrderRejectedException

        return order

    def get_balance(self):
        return self.request('GET', 'balance')

    def get_ledger(self):
        return self.request('GET', 'ledger')

    def get_instruments(self):
        """Returns a plain list of instrument codes"""
        response = self.request('GET', 'instruments')
        return [instrument.get("name") for instrument in response]


b2c2_api = B2C2Api()
