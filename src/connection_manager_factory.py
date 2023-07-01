from src.connection_manager import WireManager, CableManager


class ConnectionManagerFactory:
    @staticmethod
    def create_connection_manager(mode: str, file_name: str):
        if mode == "wire":
            return WireManager(file_name)
        elif mode == "cable":
            return CableManager(file_name)
        else:
            raise ValueError(f"Invalid connection manager type: {mode}")
