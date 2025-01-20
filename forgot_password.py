import tkinter as tk
import yagmail
import random
import re

"""
Name: ForgotPasswordPage
Purpose: This is to create a window where the user can 
navigate to and reset their master password by getting a verification email
"""
class ForgotPasswordPage(tk.Frame):
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
        self.master.title("Forgot Password")

        tk.Label(self, text="Forgot password", font=("Arial", 30)).pack(side=tk.TOP)

        tk.Label(self, text="Email Address:", font=("Arial", 11)).pack(side=tk.TOP, pady=(150, 20))

        self.__email_address = tk.StringVar()
        tk.Entry(self, textvariable=self.__email_address).pack(side=tk.TOP, pady=(20, 40))

        self.__reset_button = tk.Button(self, text="Reset Password", font=("Calibri", 15),
                                        command=self.send_email)
        self.__reset_button.pack(side=tk.TOP)

        self.__yag = yagmail.SMTP("passmasterpro1@gmail.com")
        self.__count = 0
        self.__invalid_code_label = None

        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="Forward", command=self.__controller.go_forward).pack(side=tk.BOTTOM, pady=10)

    """
    Name: send_email
    Parameters: None
    Returns: None
    Purpose: Sends the user an email with a reset code and 
    checks if they have entered it correctly
    """
    def send_email(self):
        self.__recipient = self.__email_address.get()
        self.__subject = "Reset Password Instructions"
        self.__reset_code = random.randint(100000, 999999)
        print(self.__reset_code)
        self.__contents = f"Your Password reset code is:\n{self.__reset_code}"

        try:

            if self.__count == 0 and self.check_email(self.__recipient):
                tk.Label(self, text="A code has been sent to your email address, please enter it below",
                         font=("Arial", 11)).pack()
                self.__entered_reset_code = tk.StringVar()
                tk.Entry(self, font=("", 15), textvariable=self.__entered_reset_code).pack()

                tk.Button(self, text="Verify Code", command=self.verify_code).pack(pady=10)

                self.__yag.send(to=self.__recipient, subject=self.__subject, contents=self.__contents)

            else:
                if self.__count == 0:
                    tk.Label(self, text="Invalid Email address", fg="red").pack()
                self.__reset_button["state"] = tk.NORMAL
                self.__count += 1

        except Exception as e:
            tk.Label(self, text=f"Failed to send email: {str(e)}", fg="red").pack()
            self.__reset_button["state"] = tk.NORMAL

    def check_email(self, email):
        self.__email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(self.__email_pattern, email) is not None

    def verify_code(self):
        if self.__entered_reset_code.get() == str(self.__reset_code):
            tk.Label(self, text="Correct").pack()
            self.__controller.go_to("ResetPasswordPage")
        else:
            tk.Label(self, text="Incorrect Code. Try Again.", fg="red").pack()
