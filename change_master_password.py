import tkinter as tk
import time
import Hash_SHA
from user_info import UserInfo

"""
Name: ChangeMasterPassword
Purpose: This is to create a window where the user can 
navigate to and change their master password which is
used to login to their account
"""
class ChangeMasterPassword(tk.Frame):
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
        tk.Label(self, text="Change Password", font=("", 20)).pack(pady=(50, 0))

        tk.Label(self, text="New Password:", font=("", 12)).pack(pady=(150, 0))

        self.__new_password = tk.StringVar()
        tk.Entry(self, textvariable=self.__new_password, font=("", 12)).pack(pady=(5, 0))

        tk.Label(self, text="Confirm New Password:", font=("", 12)).pack(pady=(30, 0))

        self.__confirm_new_password = tk.StringVar()
        tk.Entry(self, textvariable=self.__confirm_new_password, font=("", 12)).pack(pady=(5, 0))

        tk.Button(self, text="Change Password", font=("", 30), command=self.change_password).pack(pady=(25, 0))

        self.__error_message = tk.Label(self, text="", fg="red", font=("", 18))
        self.__error_message.pack()

        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="Forward", command=self.__controller.go_forward).pack(side=tk.BOTTOM, pady=10)

    """
    Name: change_password
    Parameters: None
    Returns: None
    Purpose: Takes the new password inputted and replaces it with the new password
    """
    def change_password(self):
        if self.__new_password.get() == self.__confirm_new_password.get():
            self.__error_message.config(text="Password changed successfully", fg="green")
            self.__master_password = Hash_SHA.hash_data(self.__new_password.get())
            self.__user_session = UserInfo()
            self.__user_id = self.__user_session.get_user_id()
            self.__values = (self.__master_password, self.__user_id)
            self.__data_to_send = {"CHANGE_MASTER": self.__values}
            self.__controller.send_request(self.__data_to_send)

            time.sleep(2.5)
            self.controller.go_to('MainPage')

        else:
            self.__error_message.config(text="Passwords do not match", fg="red")
