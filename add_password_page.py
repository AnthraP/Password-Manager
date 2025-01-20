import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import csv
import user_info

"""
Name: AddPasswordPage
Purpose: This is to create a window where the user can 
navigate to and add passwords to their collection
"""
class AddPasswordPage(tk.Frame):
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
        self.__user = user_info.UserInfo()
        self.__user_id = self.__user.get_user_id()
        self.__folders = []
        self.configure_window()

    """
    Name: configure_window
    Parameters: None
    Returns: None
    Purpose: Creates the window and all of the labels
    and buttons within it
    """
    def configure_window(self):
        tk.Label(self, text="Add passwords to collection", font=("bold", 30)).pack(side=tk.TOP, pady=(0, 150))

        tk.Label(self, text="Enter Email Address:*", font=("", 13)).pack()

        self.__email_to_save = tk.StringVar()
        self.__tk_email = tk.Entry(self, textvariable=self.__email_to_save, font=("", 13))
        self.__tk_email.pack(pady=(10, 0))

        tk.Label(self, text="Enter URL", font=("", 13)).pack(pady=(30, 0))

        self.__URL_to_save = tk.StringVar()
        self.__tk_URL = tk.Entry(self, textvariable=self.__URL_to_save, font=("", 13))
        self.__tk_URL.pack(pady=(10, 0))

        tk.Label(self, text="Enter password:* ", font=("", 13)).pack(pady=(30, 0))

        self.__password_to_save = tk.StringVar()
        self.__tk_password = tk.Entry(self, textvariable=self.__password_to_save, font=("", 13), show="*")
        self.__tk_password.pack(pady=(10, 0))

        tk.Label(self, text="Enter any notes:", font=("", 13)).pack(pady=(30, 0))

        self.__note_to_save = tk.StringVar()
        self.__tk_note = tk.Entry(self, textvariable=self.__note_to_save, font=("", 13))
        self.__tk_note.pack(pady=(10, 0))

        self.__selected_folder = tk.StringVar()
        tk.Label(self, text="Select Folder:", font=("", 13)).pack(pady=(30, 0))
        self.__folder_combobox = ttk.Combobox(self, textvariable=self.__selected_folder, font=("", 13),
                                              state="readonly")
        self.__folder_combobox.pack(pady=(10, 0))
        self.update_folders()

        tk.Label(self, text="Create New Folder:", font=("", 13)).pack(pady=(30, 0))
        self.__new_folder_name = tk.StringVar()
        self.__new_folder_entry = tk.Entry(self, textvariable=self.__new_folder_name, font=("", 13))
        self.__new_folder_entry.pack(pady=(10, 0))
        tk.Button(self, text="Create Folder", font=("", 13), command=self.create_folder).pack(pady=(10, 0))

        tk.Button(self, text="Save Password", font=("", 15), command=self.save_password).pack(pady=(40, 0))

        tk.Button(self, text="Import passwords", font=("", 15), command=self.import_passwords).pack(pady=(0, 150),
                                                                                                    side=tk.BOTTOM)

        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="Forward", command=self.__controller.go_forward).pack(side=tk.BOTTOM, pady=10)

        self.__email_incorrect = tk.Label(self, text="Email Invalid or not Entered", font=("", 11), fg="red")
        self.__password_incorrect = tk.Label(self, text="Password not entered", font=("", 11), fg="red")
    """
    Name: import_passwords
    Parameters: None
    Returns: None
    Purpose: Takes a csv file selected by the user and 
    inserts the passwords into the database line by line
    """

    def import_passwords(self):
        self.__file = fd.askopenfilename()
        with open(self.__file, mode="r") as f:
            self.__csv_file = csv.reader(f)
            next(self.__csv_file)
            for line in self.__csv_file:
                self.__WebsiteURL = line[1]
                self.__WebsiteUsername = line[2]
                self.__EncryptedPassword = line[3]
                self.__Note = line[4]
                self.__folder = "None"
                self.__values = (
                    self.__user_id, self.__WebsiteURL, self.__WebsiteUsername, self.__EncryptedPassword,
                    self.__Note, self.__folder)
                self.__data_to_send = {"INSERT": self.__values}
                self.__controller.send_request(self.__data_to_send)
    """
    Name: save_password
    Parameters: None
    Returns: None
    Purpose: Takes the entered credentials and 
    puts them into the users database
    """
    def save_password(self):
        self.__password_to_save = self.__password_to_save.get()
        self.__values = (self.__user_id, self.__URL_to_save.get(), self.__email_to_save.get(),
                         self.__password_to_save, self.__note_to_save.get(), self.__selected_folder.get())
        self.__data_to_send = {"INSERT": self.__values}
        self.__controller.send_request(self.__data_to_send)
        print("ww")
        self.clear_fields()
    """
    Name: clear_fields
    Parameters: None
    Returns: None
    Purpose: Makes all of the input fields empty
    """
    def clear_fields(self):
        self.__tk_email.delete(0, "end")
        self.__tk_URL.delete(0, "end")
        self.__tk_password.delete(0, "end")

        self.__tk_note.delete(0, "end")

    """
    Name: update_folders
    Parameters: None
    Returns: None
    Purpose: Gets all of the users folders from the server and puts it into the GUI for the user to see
    """    

    def update_folders(self):
        self.__data_to_send = {"GET_FOLDERS": self.__user_id}
        self.__folders = self.__controller.send_request(self.__data_to_send)
        self.__folders = self.__folders.get("Reply")
        self.__folder_combobox["values"] = self.__folders

    """
    Name: create_folder
    Parameters: None
    Returns: None
    Purpose: Creates a new folder for the user and updates the page to show it
    """  

    def create_folder(self):
        self.__new_folder_name = self.__new_folder_name.get().strip()
        self.__data_to_send = {"CREATE_FOLDER": [self.__user_id, self.__new_folder_name]}
        self.__controller.send_request(self.__data_to_send)
        self.update_folders()
