import tkinter as tk

import hashlib
import Hash_SHA
from user_info import UserInfo

"""
Name: LoginPage
Purpose: This is to create a window where the user can 
navigate to and login to their account or move to sign up
"""
class LoginPage(tk.Frame):
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
        self.master.title("Login Page")

        tk.Label(self, text="Login", font=("Arial", 30)).pack(side=tk.TOP, pady=50, anchor="n")

        tk.Label(self, text="Email Address:", font=("Calibri", 11)).pack(side=tk.TOP, pady=(100, 0))

        self.__email = tk.StringVar()
        tk.Entry(self, textvariable=self.__email).pack(side=tk.TOP)

        tk.Label(self, text="Password:", font=("Calibri", 11)).pack(side=tk.TOP, pady=(30, 0))

        self.__password = tk.StringVar()
        tk.Entry(self, textvariable=self.__password, show='*').pack(side=tk.TOP)

        tk.Button(self, text="Login", font=("Calibri", 20), command=self.login).pack(side=tk.TOP, pady=(50, 5))

        tk.Button(self, text="Forgot Password?", font=("Calibri", 15),
                  command=self.open_forgot_password_page).pack(side=tk.TOP, pady=(15, 20))

        tk.Button(self, text="Sign Up", font=("Calibri", 15), command=self.open_sign_up_page).pack(side=tk.TOP)

        self.__wrong_cred_label = tk.Label(self, text="Wrong Credentials, Email or Password is incorrect",
                                           font=("", 11,), fg="red")

        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="Forward", command=self.__controller.go_forward).pack(side=tk.BOTTOM, pady=10)

        tk.Button(self, text="Skip", command=self.skip).pack()

    """
    Name: open_forgot_password_page
    Parameters: None
    Returns: None
    Purpose: Goes to the forgot password page
    """
    def open_forgot_password_page(self):
        self.__controller.go_to("ForgotPasswordPage")

    """
    Name: login
    Parameters: None
    Returns: None
    Purpose: Checks if the password is correct and allows 
    the user into the main page if it is
    """
    def login(self):
        self.__password_hash = Hash_SHA.hash_data(self.__password.get())
        print(self.__password_hash)
        self.__email_string = self.__email.get()
        self.__data_to_send = {"LOGIN": [self.__email_string, self.__password_hash]}
        self.__data_recieved = self.__controller.send_request(self.__data_to_send)["Reply"]
        print(self.__data_recieved)
        if self.__data_recieved is True:
            self.__data_to_send = {"GET_USER_ID": (self.__email_string, self.__password_hash)}
            self.__user_id = self.__controller.send_request(self.__data_to_send)["Reply"]
            self.__user_session = UserInfo()

            self.__user_session.set_user_id(self.__user_id)
            self.__controller.go_to("MainPage")
        else:
            tk.Label(self, text="Incorrect Email or Password", fg="Red").pack()
            self.__email.delete(0, "end")
            self.__password.delete(0, "end")


    """
    Name: open_sign_up_page
    Parameters: None
    Returns: None
    Purpose: Goes to the sign up page
    """
    def open_sign_up_page(self):
        self.__controller.go_to("SignUpPage")


    def skip(self):
        self.__user_session = UserInfo()
        self.__user_id = 1
        self.__user_session.set_user_id(self.__user_id)
        self.__controller.go_to("MainPage")



