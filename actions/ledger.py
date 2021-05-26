from api import b2c2_api as api
from actions.main_menu import start as main_start


def start():
    ledger = api.get_ledger()
    print(ledger)
    return main_start()
