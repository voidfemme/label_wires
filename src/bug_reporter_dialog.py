import smtplib
import tkinter as tk
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# replace email and password, safely, using OAuth2.0 for gmail


class BugReporterDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Bug Reporter")

        self.parent = parent
        self.geometry("300x200")

        self.bug_report = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Describe the Bug:")
        self.label.pack(padx=10, pady=10)

        self.entry = tk.Entry(self, textvariable=self.bug_report)
        self.entry.pack(fill="both", padx=10, pady=10)

        self.report_button = tk.Button(self, text="Report", command=self.send_report)
        self.report_button.pack(padx=10, pady=10)

    def send_report(self):
        report = self.bug_report.get()
        if report:
            try:
                self.send_email(report)
                messagebox.showinfo("Success", "Bug reported successfully.")
                self.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send bug report: {e}")
        else:
            messagebox.showwarning("Warning", "Please fill in the bug report.")

    def send_email(self, report):
        msg = MIMEMultipart()
        msg["From"] = "your_email@gmail.com"
        msg["To"] = "your_email@gmail.com"
        msg["Subject"] = "New Bug Report"
        body = "Bug Report:\n\n" + report
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(msg["From"], "your_password")
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.button = tk.Button(
            self, text="Report a Bug", command=self.open_bug_reporter
        )
        self.button.pack(padx=10, pady=10)

    def open_bug_reporter(self):
        BugReporterDialog(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
