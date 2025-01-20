import tkinter as tk
import user_info
import merge_sort

"""
Name: ViewPasswordsPage
Purpose: This is to create a window where the user can 
navigate to and view their passwords
"""
class ViewPasswordsPage(tk.Frame):
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
        tk.Label(self, text="View Passwords", font=("", 30)).pack(pady=(60, 0))

        self.__frame = tk.Frame(self)
        self.__frame.pack()

        self.__scrollbar = tk.Scrollbar(self.__frame)
        self.__scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.__listbox = tk.Listbox(self.__frame, font=("", 14), width=50, height=20,
                                    yscrollcommand=self.__scrollbar.set)
        self.__listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.__scrollbar.config(command=self.__listbox.yview)

        tk.Button(self, text="Sort Ascending", command=self.sort_ascending).pack(side=tk.BOTTOM, pady=5)
        tk.Button(self, text="Sort Descending", command=self.sort_descending).pack(side=tk.BOTTOM, pady=5)

        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="Forward", command=self.__controller.go_forward).pack(side=tk.BOTTOM, pady=10)

        self.show_passwords()

    """
    Name: show_passwords
    Parameters: None
    Returns: None
    Purpose: Shows the users password on the GUI
    """

    def show_passwords(self):
        self.__user_session = user_info.UserInfo()
        self.__user_id = self.__user_session.get_user_id()
        self.__values = (self.__user_id,)
        self.__data_to_send = {"GET_PASSWORDS_WFOLDERS": self.__values}
        print(self.__data_to_send, "fff")
        self.__passwords = self.__controller.send_request(self.__data_to_send)
        print(self.__passwords)
        self.__password_list = self.__passwords["Reply"]
        if self.__password_list == 'No passwords found':
            self.__listbox.insert(tk.END, "No passwords found")
        else:
            self.update_listbox()

    """
    Name: update_listbox
    Parameters: None
    Returns: None
    Purpose: Refreshes the password areas
    """

    def update_listbox(self):
        self.__listbox.delete(0, tk.END)

        folder_dict = {}
        for password in self.__password_list:
            if password[5] != 'None':
                folder_name = password[5]
            else:
                folder_name = 'Uncategorized'
            if folder_name not in folder_dict:
                folder_dict[folder_name] = []
            folder_dict[folder_name].append(password)

        for folder_name, passwords in folder_dict.items():
            self.__listbox.insert(tk.END, folder_name)
            for password in passwords:
                website = password[1]
                username = password[2]
                actual_password = password[3]
                note = password[4] if password[4] else "No Note"
                self.__listbox.insert(tk.END, f"  {website} | {username} | {note} | Password: {actual_password}")
            self.__listbox.insert(tk.END, "")

    """
    Name: sort_ascending
    Parameters: None
    Returns: None
    Purpose: Sorts the password in ascending order
    """

    def sort_ascending(self):
        self.__password_list = merge_sort.merge_sort_ac(self.__password_list)
        self.update_listbox()

    """
    Name: sort_descending
    Parameters: None
    Returns: None
    Purpose: Sorts the password in decending order
    """

    def sort_descending(self):
        self.__password_list = merge_sort.merge_sort_de(self.__password_list)
        self.update_listbox()
