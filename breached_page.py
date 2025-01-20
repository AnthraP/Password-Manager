import tkinter as tk
import hashlib
import requests
from tkinter import messagebox
import user_info
from stack import Stack


"""
Name: BreachGUI
Purpose: This is to create a window where the user can 
navigate to and view which passwords of theirs have been 
found in a data breach
"""
class BreachGUI(tk.Frame):
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

        self.__session = user_info.UserInfo()
        self.__user_id = self.__session.get_user_id()

        tk.Label(self, text="Breached Passwords", font=("", 30)).pack(side=tk.TOP, pady=(60, 30))

        self.__frame = tk.Frame(self)
        self.__frame.pack()

        self.__scrollbar = tk.Scrollbar(self.__frame)
        self.__scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.__listbox = tk.Listbox(self.__frame, font=("", 16), width=50, height=20,
                                    yscrollcommand=self.__scrollbar.set)
        self.__listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.__scrollbar.config(command=self.__listbox.yview)

        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="Forward", command=self.__controller.go_forward).pack(side=tk.BOTTOM, pady=10)

        self.show_breached()

    """
    Name: show_breached
    Parameters: None
    Returns: None
    Purpose: Requests the users passwords from the server 
    and uses them to request the HIBP API for the breach report
    """
    def show_breached(self):
        self.__user_session = user_info.UserInfo()
        self.__user_id = self.__user_session.get_user_id()
        self.__data_to_send = {"API_BREACHED_PASSWORD": self.__user_id}
        self.__breached_info = self.__controller.send_request(self.__data_to_send)["Reply"]

        if self.__breached_info == "No passwords found":
            self.__listbox.insert(tk.END, "No passwords found")
        else:
            for info in self.__breached_info:
                self.__listbox.insert(tk.END, info)
