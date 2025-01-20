import tkinter as tk

"""
Name: SettingPage
Purpose: This is to create a window where the user can 
navigate to adn access their settings
"""
class SettingsPage(tk.Frame):
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
        self.__controller.title("Settings Page")
        self.configure(bg="white")

        tk.Label(self, text="Settings", font=("", 30), bg="white").pack(pady=(60, 30))

        tk.Button(self, text="Logout", font=("", 16), command=self.logout).pack(pady=10)

        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="Forward", command=self.__controller.go_forward).pack(side=tk.BOTTOM, pady=10)

    """
    Name: logout
    Parameters: None
    Returns: None
    Purpose: Logs out the user
    """

    def logout(self):
        self.__controller.go_to("LoginPage")

