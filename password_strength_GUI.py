import tkinter as tk
import password_strength as ps

"""
Name: PasswordStrengthGUI
Purpose: This is to create a window where the user can 
navigate to and enter a password to be strength tested
"""

class PasswordStrengthGUI(tk.Frame):
    """
    Name: __init__
    Parameters: parent: Class, controller: CLass
    Returns: None
    Purpose: Constructor of the object to start the
    window and initialise the values
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.__controller = controller
        self.configure_window()

    """
    Name: configure_window
    Parameters: None
    Returns: None
    Purpose: Creates the window and all of the labels
    and buttons within it
    """

    def configure_window(self):
        self.__controller.title("Password Strength")

        tk.Label(self, text="Password Strength", font=("", 30)).pack(side=tk.TOP, pady=(60, 70))

        self.__check_button = tk.IntVar()
        tk.Checkbutton(self, text="Hide password", variable=self.__check_button, font=("", 16), command=self.hide_password).pack(pady=(30, 0))

        self.__password = tk.StringVar()
        self.__password_label = tk.Entry(self, textvariable=self.__password, font=("", 16))
        self.__password_label.pack(pady=(30, 0))

        tk.Button(self, text="Get Results", command=self.tester, font=("", 16)).pack(pady=(20, 0))

        self.__score_label = tk.Label(self, text="", font=("", 16))
        self.__score_label.pack(pady=(30, 0))

        tk.Button(self, text="Use from collection", font=("", 16), command=self.use_collection).pack()

        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="Forward", command=self.__controller.go_forward).pack(side=tk.BOTTOM, pady=10)

    """
    Name: tester
    Parameters: None
    Returns: None
    Purpose: Retrieves the strength score of the password entered
    """

    def tester(self):
        self.__score = ps.strength_checker(self.__password.get())

        self.__score_label.config(text=f"Score: {self.__score}")

    """
    Name: hide_password
    Parameters: None
    Returns: None
    Purpose: Hides the password, showing only asterix's
    """

    def hide_password(self):
        if self.__check_button.get() == 1:
            self.__password_label.config(show="*")
        else:
            self.__password_label.config(show="")

    """
    Name: use_collection
    Parameters: None
    Returns: None
    Purpose: Sends the user to a page where the can view the strength of 
    their currently used passwords
    """

    def use_collection(self):
        self.__controller.go_to("CollectionGUI")



