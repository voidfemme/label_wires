#!/usr/bin/env python3
# Workers of the world, Unite!
import os
import tkinter as tk
import tkinter.messagebox
from tkinter import scrolledtext, simpledialog
from src.wire_app import WireApp


def start_app():
    file_name = ""
    while not file_name:
        file_name = simpledialog.askstring(
            "Wire Manager", "Please enter the name of the file (without extension)"
        )
        if not file_name:
            tkinter.messagebox.showwarning(
                title="Invalid Input",
                message="Please provide a valid file name.",
            )
        else:
            data_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "label_wires", "data"
            )
            file_name = os.path.join(data_dir, file_name)

    app = WireApp(file_name)

    app.csv_file_name.set(file_name)

    app.mainloop()


if __name__ == "__main__":
    start_app()
