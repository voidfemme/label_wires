class Settings:
    def __init__(self):
        self.default_directory = ""
        self.default_mode = "wire"

    def get_default_directory(self):
        return self.default_directory

    def set_default_directory(self, path):
        self.default_directory = path

    def get_default_mode(self):
        return self.default_mode

    def set_default_mode(self, mode):
        self.default_mode = mode


# Create a global settings object that can be imported in other modules
settings = Settings()
