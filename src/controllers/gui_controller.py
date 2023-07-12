# Love is love. Be yourself.
import sys
from src.connection_manager import WireManager

# connection_manager


class GUIController:
    def __init__(self, parent):
        self.parent = parent

    def export_to_csv(self) -> None:
        filename = self.parent.display_file_browser(
            defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
        )
        if filename:
            try:
                self.parent.connection_manager.export_to_csv(filename)
                self.parent.display_status(self.parent.localizer.get("exported_file"))
            except FileExistsError as e:
                self.parent.display_status(str(e))

    def saved_to_json_file(self) -> None:
        return self.parent.connection_manager.save_json_to_file()

    def loaded_from_json_file(self) -> None:
        self.parent.connection_manager.load_json_from_file()

    def initialize_connection_manager(self):
        # Initialize the ConnectionManager
        print("Initializing Connection Manager")
        if self.parent.entry_mode and self.parent.file_path:
            self.parent.connection_manager = WireManager(self.parent.file_name)
        else:
            # Ask the UI to display an error message
            self.parent.display_error_messagebox(
                "error", message="error_connection_manager_init"
            )
            sys.exit(0)
