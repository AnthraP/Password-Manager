import tkinter as tk
import Hash_SHA


class ResetPasswordPage(tk.Frame):
    """
    Name: __init__
    Parameters: parent: Class, controller: Class
    Returns: None
    Purpose: Inherits from the parent class and starts the window
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.__controller = controller
        self.configure_window()

    """
    Name: configure_window
    Parameters: None
    Returns: None
    Purpose: Shows the GUI for the user
    """

    def configure_window(self):
        tk.Label(self, text="Reset Password", font=("Arial", 30)).pack(side=tk.TOP, pady=(20, 10))

        tk.Label(self, text="Email Address:", font=("Arial", 11)).pack(pady=(20, 5))
        self.__email_address = tk.StringVar()
        tk.Entry(self, textvariable=self.__email_address, font=("Arial", 12)).pack(pady=(0, 10))

        tk.Label(self, text="New Password:", font=("Arial", 11)).pack(pady=(10, 5))
        self.__new_password = tk.StringVar()
        tk.Entry(self, textvariable=self.__new_password, font=("Arial", 12), show="*").pack(pady=(0, 10))

        tk.Label(self, text="Confirm Password:", font=("Arial", 11)).pack(pady=(10, 5))
        self.__confirm_password = tk.StringVar()
        tk.Entry(self, textvariable=self.__confirm_password, font=("Arial", 12), show="*").pack(pady=(0, 20))

        tk.Button(self, text="Reset Password", font=("Calibri", 15), command=self.reset_password).pack(pady=(10, 20))

        # Back button
        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)

    """
    Name: reset_password
    Parameters: None
    Returns: None
    Purpose: Validates inputs and processes password reset
    """

    def reset_password(self):
        email = self.__email_address.get()
        new_password = self.__new_password.get()
        confirm_password = self.__confirm_password.get()
        confirm_password_hash = Hash_SHA.hash_data(confirm_password)

        if new_password != confirm_password:
            tk.Label(self, text="Passwords do not match", fg="red").pack()
        else:
            tk.Label(self, text="Password reset successfully!", fg="green").pack()

            values = (confirm_password_hash, email)
            data_to_send = {"CHANGE_MASTER_PASSWORD_FORGOT": values}
            self.__controller.send_request(data_to_send)


