#!/usr/bin/env python3
# Workers of the world, Unite!
import os
import sys
import tkinter.messagebox
from src.wire_app import WireApp
from src.dialog import CustomDialog
from src.wire_manager import GUIWireManager


def start_app():
    file_name = ""
    while not file_name:
        dialog = CustomDialog(None)
        file_name = dialog.result

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
                print(f"Data dir: {data_dir}")
                file_name = os.path.join(data_dir, file_name + ".json")
                print(f"File name: {file_name}")

    wire_manager = GUIWireManager(file_name, "data")
    app = WireApp(wire_manager, file_name)
    app.wire_manager.load_from_file()

    app.json_file_name.set(file_name)

    app.mainloop()


if __name__ == "__main__":
    start_app()
