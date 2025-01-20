import tkinter as tk
from Hash_SHA import hash_data


"""
Name: SignUpPage
Purpose: This is to create a window where the user can sign up to the application
"""

class SignUpPage(tk.Frame):
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
        tk.Label(self, text="Sign Up", font=("Arial", 30)).pack(side=tk.TOP, pady=50)

        tk.Label(self, text="Forname*", font=("", 15)).pack(side=tk.TOP, pady=(100, 0))

        self.__forname = tk.StringVar()
        self.__tkforname = tk.Entry(self, textvariable=self.__forname, font=("", 15))
        self.__tkforname.pack(side=tk.TOP)

        tk.Label(self, text="Surname*", font=("", 15)).pack(side=tk.TOP, pady=(30, 0))

        self.__surname = tk.StringVar()
        self.__tksurname = tk.Entry(self, textvariable=self.__surname, font=("", 15))
        self.__tksurname.pack(side=tk.TOP)

        tk.Label(self, text="Email Address:*", font=("", 15)).pack(side=tk.TOP, pady=(30, 0))

        self.__email_address = tk.StringVar()
        self.__tkemail = tk.Entry(self, textvariable=self.__email_address, font=("", 15))
        self.__tkemail.pack(side=tk.TOP)

        tk.Label(self, text="Password:*", font=("", 15)).pack(side=tk.TOP, pady=(30, 0))

        self.__password = tk.StringVar()
        self.__tkpassword = tk.Entry(self, textvariable=self.__password, font=("", 15))
        self.__tkpassword.pack(side=tk.TOP)

        tk.Button(self, text="Sign Up", font=("", 15), command=self.sign_up_button_clicked).pack(side=tk.TOP, pady=30)

        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="Forward", command=self.__controller.go_forward).pack(side=tk.BOTTOM, pady=10)

        self.__error_label = tk.Label(self, text="", font=("", 10), fg="red")
        self.__error_label.pack()

    """
    Name: sign_up_button_clicked
    Parameters: None
    Returns: None
    Purpose: Checks if the email is already being used 
    and if not, creates a new account 
    """

    def sign_up_button_clicked(self):
        if not (self.__email_address.get() and self.__password.get() and self.__surname.get() and self.__forname.get()):
            self.__error_label.config(text="Please fill in all details")
            return

        if self.email_in_use() is True:
            self.__error_label.config(text="Account already created with this email, enter a different one and try again")
        else:
            self.create_user()
            self.__tkforname.delete(0, tk.END)
            self.__tksurname.delete(0, tk.END)
            self.__tkemail.delete(0, tk.END)
            self.__tkpassword.delete(0, tk.END)
            self.__controller.go_to("LoginPage")

    """
    Name: create_user
    Parameters: None
    Returns: None
    Purpose: Creates a new user by querying the database and 
    inserting the new information into it
    """

    def create_user(self):
        self.__hash_password = hash_data(self.__password.get())
        self.__values = (self.__forname.get(), self.__surname.get(), self.__hash_password, self.__email_address.get().lower())
        self.__data_to_send = {"SIGN_UP": self.__values}
        self.__controller.send_request(self.__data_to_send)
        self.__data_to_send = {"GET_USER_ID": (self.__email_address.get(), self.__hash_password)}
        self.__user_id = self.__controller.send_request(self.__data_to_send)["Reply"]
        self.__data_to_send = {"CREATE_FOLDER": [self.__user_id, "None"]}
        self.__controller.send_request(self.__data_to_send)
        self.__controller.go_to("LoginPage")

    """
    Name: email_in_use
    Parameters: None
    Returns: Boolean
    Purpose: Checks if the email is already in the 
    database and returns the appropriate boolean value
    """

    def email_in_use(self):
        self.__data_to_send = {"USED_EMAIL": (self.__email_address.get().lower(),)}
        self.__response = self.__controller.send_request(self.__data_to_send)
        return self.__response["Reply"]





