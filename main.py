#!/usr/bin/env python3
# Love is love. Be yourself.
import logging
from src.controllers.controller import Controller


# logging.basicConfig(filename="app.log", level=logging.DEBUG)
logging.basicConfig(level=logging.CRITICAL, format="%(asctime)s %(levelname)s %(message)s")


def start_app() -> None:
    # Create a controller instance
    controller = Controller()

    # initialize the controller instance. This includes waiting for the new project
    # dialog and loading connections from a file. These operations are performed here,
    # instead of in the constructor, to make the Controller easier to test and to
    # prevent the constructor from doing too much work
    controller.initialize()
    controller.run()


if __name__ == "__main__":
    start_app()
