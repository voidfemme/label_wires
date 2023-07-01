#!/usr/bin/env python3
# Love is love. Be yourself.
import logging
from src.connection_app import ConnectionApp


logging.basicConfig(filename="app.log", level=logging.DEBUG)


def start_app():
    app = ConnectionApp()
    app.mainloop()


if __name__ == "__main__":
    start_app()
