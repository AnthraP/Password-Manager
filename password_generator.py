import tkinter as tk
import string
import random



"""
Name: GeneratePasswordPage
Purpose: This is to create a window where the user can 
navigate to and generate a random password
"""
class GeneratePasswordPage(tk.Frame):
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

        self.__possible_set = [string.ascii_uppercase, string.ascii_lowercase, string.punctuation, string.digits]
        self.__password = ""
        self.__error_label = None

        self.configure_window()

    """
    Name: configure_window
    Parameters: None
    Returns: None
    Purpose: Creates the window and all of the labels
    and buttons within it
    """

    def configure_window(self):
        self.__controller.title("Password Generator")

        self.__check_state_1 = tk.IntVar()
        self.__checkbox1 = tk.Checkbutton(self, text="Uppercase", font=("Times New Roman", 11), variable=self.__check_state_1)
        self.__checkbox1.pack(pady=5)

        self.__check_state_2 = tk.IntVar()
        self.__checkbox2 = tk.Checkbutton(self, text="Lowercase", font=("Times New Roman", 11), variable=self.__check_state_2)
        self.__checkbox2.pack(pady=5)

        self.__check_state_3 = tk.IntVar()
        self.__checkbox3 = tk.Checkbutton(self, text="Special Characters", font=("Times New Roman", 11), variable=self.__check_state_3)
        self.__checkbox3.pack(pady=5)

        self.__check_state_4 = tk.IntVar()
        self.__checkbox4 = tk.Checkbutton(self, text="Numbers", font=("Times New Roman", 11), variable=self.__check_state_4)
        self.__checkbox4.pack(pady=5)

        self.__password_length_scale = tk.Scale(self, from_=1, to=99, orient="horizontal", label="Password Length")
        self.__password_length_scale.pack(pady=5)

        self.__generate_button = tk.Button(self, text="Generate!", font=("Arial", 18), command=self.password)
        self.__generate_button.pack(pady=15)

        self.__copy_button = tk.Button(self, text="Copy password", font=("Arial", 10), command=self.copy_password)
        self.__copy_button.pack(pady=15)

        tk.Button(self, text="Back", command=self.__controller.go_back).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="Forward", command=self.__controller.go_forward).pack(side=tk.BOTTOM, pady=10)

        self.__label = tk.Label(self, text="", font=("Arial", 14))
        self.__label.pack(padx=20, pady=15)

    """
    Name: password
    Parameters: None
    Return: None
    Purpose: Generates the password for the user by checking the criteria requested and showing it to the user onscreen
    """

    def password(self):
        if self.__error_label:
            self.__error_label.destroy()
            self.__error_label = None


        char_set = ""
        self.__password = ""

        if self.__check_state_1.get() == 1:
            char_set += self.__possible_set[0]
        if self.__check_state_2.get() == 1:
            char_set += self.__possible_set[1]
        if self.__check_state_3.get() == 1:
            char_set += self.__possible_set[2]
        if self.__check_state_4.get() == 1:
            char_set += self.__possible_set[3]

        if not char_set:
            self.__error_label = tk.Label(self, text="You must select at least one box", font=("Calibri", 14), fg="red")
            self.__error_label.pack(pady=(10, 0))
            return

        length = self.__password_length_scale.get()
        self.__password = ''.join(random.choices(char_set, k=length))
        self.__label.config(text=self.__password)

    """
    Name: copy_password
    Parameters: None
    Returns: None
    Purpose: Copies the generated password to the clipboard
    """

    def copy_password(self):
        if self.__password:
            self.clipboard_clear()
            self.clipboard_append(self.__password)
            tk.messagebox.showinfo("Copied", "Password copied to clipboard!")
            self.update()
        else:
            tk.messagebox.showerror("Error", "No password to copy. Please generate one first.")





