import os
from tkinter import filedialog, simpledialog, ttk


class CustomDialog(simpledialog.Dialog):
    def body(self, master):
        ttk.Label(
            master,
            text="Please enter the name of the file to create (without extension):",
        ).grid(row=0)

        self.e1 = ttk.Entry(master)
        self.e1.grid(row=1, padx=10, pady=10)

        self.b1 = ttk.Button(master, text="Browse", command=self.browse_file)
        self.b1.grid(row=2, padx=10, pady=10)

        return self.e1

    def browse_file(self):
        file_name = filedialog.askopenfilename(
            initialdir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "src", "data"
            ),
            title="Select file",
            filetypes=(("CSV files", "*.csv"), ("all files", "*.*")),
        )
        if file_name:
            self.e1.delete(0, "end")
            self.e1.insert(0, file_name)

    def apply(self):
        self.result = self.e1.get()
