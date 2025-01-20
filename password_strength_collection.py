import tkinter as tk
import user_info
import password_strength as ps

"""
Name: CollectionGUI
Purpose: This is to create a window where the user can navigate to and 
test the strength of the users passwords that are stored in their collection
"""
class CollectionGUI(tk.Frame):
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
        self.__controller.title("Password Strength Checker")

        tk.Label(self, text="Stored Passwords and Strength", font=("", 30)).pack(side=tk.TOP, pady=(60, 30))

        self.__frame = tk.Frame(self)
        self.__frame.pack()

        self.__scrollbar = tk.Scrollbar(self.__frame)
        self.__scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.__listbox = tk.Listbox(self.__frame, font=("", 16), width=50, height=20, yscrollcommand=self.__scrollbar.set)
        self.__listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.__scrollbar.config(command=self.__listbox.yview)

        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="Forward", command=self.__controller.go_forward).pack(side=tk.BOTTOM, pady=10)

        self.display_password_strengths()

    """
    Name: display_password_strengths
    Parameters: None
    Returns: None
    Purpose: Requests the users passwords and gets the strength 
    of them, this is then displayed for the user
    """

    def display_password_strengths(self):
        self.__user_session = user_info.UserInfo()
        self.__user_id = self.__user_session.get_user_id()
        self.__values = (self.__user_id,)
        self.__data_to_send = {"GET_PASSWORDS": self.__values}
        self.__passwords = self.__controller.send_request(self.__data_to_send)
        self.__passwords = self.__passwords["Reply"]

        if self.__passwords == "No passwords found":
            self.__listbox.insert(tk.END, "No passwords found")
        else:

            for password_tuple in self.__passwords:
                self.__password = password_tuple[0]
                self.__score = ps.strength_checker(self.__password)
                self.__listbox.insert(tk.END, f"Password: {self.__password} | Strength: {self.__score}")





