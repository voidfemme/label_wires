#!/usr/bin/env python3
# Love is love. Be yourself.
import os
import sys
import tkinter as tk
import tkinter.messagebox
from src.wire_app import WireApp
from src.dialog import StartupDialog
from src.wire_manager import WireManager, CableManager


def start_app():
    root = tk.Tk()
    root.withdraw()
    file_name = ""
    entry_mode = ""
    while not file_name:
        dialog = StartupDialog(None)
        if dialog.result is None:
            sys.exit()
        file_name = dialog.result.get("file_name")
        print(f"file_name: {file_name}")
        entry_mode = dialog.result.get("mode")
        print(f"entry_mode: {entry_mode}")

        if file_name is None:
            sys.exit()

        if not file_name:
            tkinter.messagebox.showwarning(
                title="Invalid Input",
                message="Please provide a valid file name.",
            )
        else:
            # if selected from the file dialog, the file_name already contains the full path
            # else append the relative path
            if not os.path.isabs(file_name):
                data_dir = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "src", "data"
                )
                file_name = os.path.join(data_dir, file_name)
                if entry_mode == "wire":
                    file_name += ".wir"
                elif entry_mode == "cable":
                    file_name += ".cab"
                else:
                    file_name += ".json"

            if not os.path.exists(file_name):
                # Create file
                with open(file_name, "w") as f:
                    pass
            if entry_mode == "wire":
                connection_manager = WireManager(file_name, entry_mode)
            elif entry_mode == "cable":
                connection_manager = CableManager(file_name, entry_mode)
            else:
                raise ValueError(f"Invalid mode: {entry_mode}")

            app = WireApp(connection_manager, file_name, entry_mode)
            app.wire_manager.load_from_file()
            app.mainloop()

    return root


if __name__ == "__main__":
    root = start_app()
    root.destroy()
