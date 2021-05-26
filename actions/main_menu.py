from bullet import Bullet
from styles import bullet_style

REQUEST_QUOTE_ACTION = "Request a quote"
TRANSACTIONS_LIST_ACTION = "List my transactions"
EXIT_ACTION = "Exit"


def start():
    main_cli = Bullet(
        prompt="\nWhat would you like to do? \n",
        choices=[REQUEST_QUOTE_ACTION, TRANSACTIONS_LIST_ACTION, EXIT_ACTION],
        **bullet_style
    )

    result = main_cli.launch()

    if result == REQUEST_QUOTE_ACTION:
        from actions import request_quote
        request_quote.start()
    elif result == TRANSACTIONS_LIST_ACTION:
        from actions import ledger
        ledger.start()
    elif result == EXIT_ACTION:
        print("Goodbye!")

