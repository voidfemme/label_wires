#!/usr/bin/env python3
# Love is love. Be yourself.
import logging
from src.connection_app import ConnectionApp
from src.settings import Settings


logging.basicConfig(filename="app.log", level=logging.DEBUG)


def start_app():
    settings = Settings()
    app = ConnectionApp(language=settings.get("language"))
    app.mainloop()


if __name__ == "__main__":
    start_app()
