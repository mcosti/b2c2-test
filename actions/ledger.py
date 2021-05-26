from api import b2c2_api as api
from actions.main_menu import start as main_start


def start():
    api.get_ledger()  # logging will be handled by the api class, I won't continue developing this, I'm out of time
    # The response could be transformed into a menu
    return main_start()
