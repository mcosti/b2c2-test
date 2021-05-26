import logging
from bullet import Bullet, Numbers, YesNo, Input

from actions.main_menu import start as main_start
from api import b2c2_api as api
from exceptions import OrderRejectedException, QuoteExpiredException, B2C2Exception
from styles import bullet_style

BUY_CHOICE = "BUY"
SELL_CHOICE = "SELL"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

instruments = api.get_instruments()


def start():
    print("List of the available instruments: \n" + ", ".join(instruments))

    instrument_code = Input(prompt="Type the instrument: ").launch()

    if instrument_code not in instruments:
        # Small bug here not allowing to close the program until an instrument is written
        print("Invalid instrument, please choose one from the list. \n")
        return start()

    side = Bullet(
        prompt="Buy or sell?",
        choices=[BUY_CHOICE, SELL_CHOICE],
        **bullet_style
    ).launch()
    quantity = Numbers("Quantity: ", type=float).launch()
    print("Your choices", instrument_code, side, quantity)

    try:
        quote = api.request_quote(instrument=instrument_code, side=side, quantity=quantity)
        print(f"Returned quote: \n {quote.__dict__} \n")
    except B2C2Exception as e:
        print(f"Encountered exception: {e} \n")
        return start()

    should_continue = YesNo("Do you want to continue?").launch()
    if not should_continue:
        print("Going back to main menu. \n")
        return main_start()

    if quote.is_expired:
        print("Quote has expired, re-start process. (exception handled before API call) \n")
        return start()

    try:
        order = api.create_order(quote)
        print(order.__dict__)  # lazy way of printing
    except OrderRejectedException:
        print("Order rejected, re-starting process. \n")
        return start()
    except QuoteExpiredException:
        print("The quote has expired, re-starting process. \n")
        return start()
    except B2C2Exception as e:
        print(f"Encountered exception: {e} \n")
        return start()

    balance = api.get_balance()
    print(f"Balance: \n {balance} \n Going back to the main menu. \n")
    return main_start()
