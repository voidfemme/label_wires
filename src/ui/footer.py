import tkinter as tk


class Footer(tk.Frame):
    def __init__(self, parent, controller, localizer, settings):
        super().__init__(parent)
        self.controller = controller
        self.localizer = localizer
        self.settings = settings

        self.status_label = tk.Label(self, text="")
        self.status_label.grid(row=1, column=0, padx=10)

        # Replace with localization
        self.display_status("Welcome to WireLab")

    def display_status(self, message) -> None:
        # Update the status label with the message
        self.status_label["text"] = message

        # Clear the status label after 5 seconds
        self.after(5000, lambda: self.status_label.config(text=""))
