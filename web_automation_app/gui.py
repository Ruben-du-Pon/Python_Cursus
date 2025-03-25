import tkinter as tk
from main import WebAutomation


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Web Automation App")
        self._create_login_frame()
        self._create_form_frame()
        self._create_buttons()

    def _create_login_frame(self) -> None:
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)

        tk.Label(self.login_frame, text="Username ").grid(row=0,
                                                          column=0,
                                                          sticky="w")
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_username.grid(row=0, column=1, sticky="ew")

        tk.Label(self.login_frame, text="Password ").grid(row=1,
                                                          column=0,
                                                          sticky="w")
        self.entry_password = tk.Entry(self.login_frame,
                                       show="*")
        self.entry_password.grid(row=1, column=1, sticky="ew")

    def _create_form_frame(self) -> None:
        self.form_frame = tk.Frame(self.root)
        self.form_frame.pack(padx=10, pady=10)

        tk.Label(self.form_frame, text="Full Name ").grid(row=0,
                                                          column=0,
                                                          sticky="w")
        self.entry_fullname = tk.Entry(self.form_frame)
        self.entry_fullname.grid(row=0, column=1, sticky="ew")

        tk.Label(self.form_frame, text="Email ").grid(row=1,
                                                      column=0,
                                                      sticky="w")
        self.entry_email = tk.Entry(self.form_frame)
        self.entry_email.grid(row=1, column=1, sticky="ew")

        tk.Label(self.form_frame, text="Current Address ").grid(row=2,
                                                                column=0,
                                                                sticky="w")
        self.entry_current_address = tk.Entry(self.form_frame)
        self.entry_current_address.grid(row=2, column=1, sticky="ew")

        tk.Label(self.form_frame, text="Permanent Address ").grid(row=3,
                                                                  column=0,
                                                                  sticky="w")
        self.entry_permanent_address = tk.Entry(self.form_frame)
        self.entry_permanent_address.grid(row=3, column=1, sticky="ew")

    def _create_buttons(self) -> None:
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(padx=10, pady=10)

        tk.Button(self.button_frame, text="Submit",
                  command=self.get_data).grid(row=0, column=0, padx=5)
        tk.Button(self.button_frame, text="Download",
                  command=self.download).grid(row=0, column=1, padx=5)
        tk.Button(self.button_frame, text="Close Browser",
                  command=self.close_browser).grid(row=0, column=2, padx=5)

    def get_data(self) -> None:
        username = self.entry_username.get()
        password = self.entry_password.get()
        fullname = self.entry_fullname.get()
        email = self.entry_email.get()
        current_address = self.entry_current_address.get()
        permanent_address = self.entry_permanent_address.get()

        self.automation = WebAutomation()
        self.submit_data(username, password, fullname, email,
                         current_address, permanent_address)

    def submit_data(self, username: str, password: str, fullname: str,
                    email: str, current_address: str,
                    permanent_address: str) -> None:
        self.automation.login(username, password)
        self.automation.fill_form(
            fullname, email, current_address, permanent_address)

    def download(self) -> None:
        self.automation.download()

    def close_browser(self) -> None:
        self.automation.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
