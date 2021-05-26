import logging
from bullet import Bullet, Numbers, YesNo

from actions.main_menu import start as main_start
from api import b2c2_api as api
from exceptions import OrderRejectedException, QuoteExpiredException
from styles import bullet_style

BUY_CHOICE = "BUY"
SELL_CHOICE = "SELL"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

instruments = api.get_instruments()


def start():
    print("List of available instruments", instruments)
    instrument_code = Bullet(
        prompt="Name of the instrument: ",
        choices=instruments,
        **bullet_style
    ).launch()

    side = Bullet(
        prompt="Buy or sell?",
        choices=[BUY_CHOICE, SELL_CHOICE],
        **bullet_style
    ).launch()
    quantity = Numbers("Quantity: ", type=float).launch()
    print("Your choices", instrument_code, side, quantity)

    quote = api.request_quote(instrument=instrument_code, side=side, quantity=quantity)

    should_continue = YesNo("Do you want to continue?").launch()
    if not should_continue:
        print("Going back to main menu")
        return main_start()

    if quote.is_expired:
        print("Quote has expired, re-start process.")
        return start()

    try:
        order = api.create_order(quote)
    except OrderRejectedException:
        logger.error("Order rejected")
        return start()
    except QuoteExpiredException:
        logger.error("The quote has expired")
        return start()

    balance = api.get_balance()  # printing is handled by the api class (for now)
    print("Going back to main menu")
    return main_start()
