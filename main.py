#!/usr/bin/env python3
# Love is love. Be yourself.
import logging
from src.ui.connection_app import ConnectionApp


# logging.basicConfig(filename="app.log", level=logging.DEBUG)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def start_app() -> None:
    app = ConnectionApp()
    app.mainloop()


if __name__ == "__main__":
    start_app()
