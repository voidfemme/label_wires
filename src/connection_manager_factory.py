from src.connection_manager import ConnectionManager, WireManager, CableManager


class ConnectionManagerFactory:
    @staticmethod
    def create_connection_manager(mode: str, file_name: str) -> ConnectionManager:
        if mode == "wire":
            return WireManager(file_name)
        elif mode == "cable":
            return CableManager(file_name)
        else:
            raise ValueError(f"Invalid connection manager type: {mode}")

    # Remember the Liskov Substitution Principle: a base class should be able
    # to be replaced with any of its subclasses without altering the properties
    # of the program. Hence, if a function expects a 'ConnectionManager', it
    # should be fine with receiving a 'WireManager' or 'CableManager' (or any
    # other subclass of 'ConnectionManager').
