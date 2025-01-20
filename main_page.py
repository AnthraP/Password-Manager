import tkinter as tk
import time


"""
Name: MainPage
Purpose: This is to create a window where the user can navigate to all functions of the application
"""
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.__controller = controller
        self.configure_window()
        self.__timeout = 20
        self.__last_activity = time.time()
        self.bind_all("<Any-KeyPress>", self.reset_timer)
        self.bind_all("<Motion>", self.reset_timer)
        self.auto_lock_timer()

    """
    Name: configure_window
    Parameters: None
    Returns: None
    Purpose: Constructor of the object to start the window and initialise variables
    """

    def configure_window(self):
        self.__controller.title("Main Page")

        tk.Button(self, text="Settings", font=("", 18), command=self.settings).pack(side=tk.RIGHT, anchor="ne")

        tk.Button(self, text="Add New Password", font=("", 20), command=self.passwords).pack(anchor="nw", pady=(200, 30))

        tk.Button(self, text="View Passwords", font=("", 20), command=self.view_password).pack(anchor="nw")

        tk.Button(self, text="Generate Password", font=("", 20), command=self.generate_password).pack(anchor="nw", pady=30)

        tk.Button(self, text="Test Strength of Password", font=("", 20), command=self.open_password_strength_page).pack(anchor="nw")

        tk.Button(self, text="Test if passwords have been breached", font=("", 20), command=self.open_breach_page).pack(anchor="nw")

        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="Forward", command=self.__controller.go_forward).pack(side=tk.BOTTOM, pady=10)
    
    """
    Name: settings
    Parameters: None
    Returns: None
    Purpose: Sends the user to the settings page
    """

    def settings(self):
        self.__controller.go_to("SettingsPage")

    """
    Name: passwords
    Parameters: None
    Returns: None
    Purpose: Sends the user to the page where they can add a new password
    """

    def passwords(self):
        self.__controller.go_to("AddPasswordPage")

    """
    Name: generate_password
    Parameters: None
    Returns: None
    Purpose: Sends the user to the page to generate a new password
    """

    def generate_password(self):
        self.__controller.go_to("GeneratePasswordPage")

    """
    Name: open_password_strength_page
    Parameters: None
    Returns: None
    Purpose: Sends the user to the page to test the strength of their passwords
    """

    def open_password_strength_page(self):
        self.__controller.go_to("PasswordStrengthGUI")

    """
    Name: view_passwords
    Parameters: None
    Returns: None
    Purpose: Sends the user to the page where they can view their passwords
    """

    def view_password(self):
        self.__controller.go_to("ViewPasswordsPage")

    """
    Name: open_breach_page
    Parameters: None
    Returns: None
    Purpose: Sends the user to the page where they can see if there passwords have been in a breach
    """

    def open_breach_page(self):
        self.__controller.go_to("BreachGUI")

    def check_movement(self):
        time_spent = time.time() - self.__last_activity
        if time_spent >= self.__timeout:
            self.login_page()
        else:
            self.auto_lock_timer()

    def reset_timer(self, event=None):
        self.__last_activity = time.time()

    def auto_lock_timer(self):
        self.after(1000, self.check_movement)

    def login_page(self):
        self.__controller.go_to("LoginPage")





