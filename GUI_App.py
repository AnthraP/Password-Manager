import tkinter as tk
from login_page import LoginPage
from sign_up_page import SignUpPage
from add_password_page import AddPasswordPage
from change_master_password import ChangeMasterPassword
from forgot_password import ForgotPasswordPage
from main_page import MainPage
from password_generator import GeneratePasswordPage
from password_strength_collection import CollectionGUI
from password_strength_GUI import PasswordStrengthGUI
from settings_page import SettingsPage
from view_passwords import ViewPasswordsPage
from forgot_change_password import ResetPasswordPage
from stack import Stack
from breached_page import BreachGUI
import socket
import json
import pyAesCrypt
import io


"""
Name: MyApp
Purpose: Root for all windows in the GUI, handles all the 
connections with the server and stack
"""
class MyApp(tk.Tk):
    """
    Name: __init__
    Parameters: None
    Returns: None
    Purpose: Initialises values and objects, registers windows
    and connects the client to the server
    """
    def __init__(self):
        super().__init__()

        self.__socket = None
        self.__host = "127.0.0.1"
        self.__port = 58868
        self.__buffer_size = 1024
        self.__password = "8^Ri%9B0aqtB"

        self.__history_stack = Stack()
        self.__forward_stack = Stack()

        self.title("Password Manager")
        self.state("zoomed")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.__current_frame = None

        self.server_connect()

        self.__page_dict = {
            "LoginPage": LoginPage,
            "BreachGUI": BreachGUI,
            "SignUpPage": SignUpPage,
            "AddPasswordPage": AddPasswordPage,
            "ChangeMasterPassword": ChangeMasterPassword,
            "ForgotPasswordPage": ForgotPasswordPage,
            "MainPage": MainPage,
            "GeneratePasswordPage": GeneratePasswordPage,
            "CollectionGUI": CollectionGUI,
            "PasswordStrengthGUI": PasswordStrengthGUI,
            "SettingsPage": SettingsPage,
            "ViewPasswordsPage": ViewPasswordsPage,
            "ResetPasswordPage": ResetPasswordPage
        }

        self.show_frame("LoginPage")

    """
    Name: server_connect
    Parameters: None
    Returns: None
    Purpose: Connects the client to the server
    """
    def server_connect(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self.__host, self.__port))
            print(f"Connected to server at {self.__host}:{self.__port}")
        except socket.error as e:
            tk.messagebox.showerror("Connection Error", "Server is currently not available")
            self.destroy()

    """
    Name: send_request
    Parameters: request: Dict
    Returns: response: Dict
    Purpose: Sends a request from the client to the server and receives a response
    """
    def send_request(self, request):
        print("THIUS REQUEST FRFR GORATEDF", request)
        try:
            self.__request = json.dumps(request).encode('utf-8')
            fIn = io.BytesIO(self.__request)
            fCiph = io.BytesIO()
            pyAesCrypt.encryptStream(fIn, fCiph, self.__password, self.__buffer_size)
            dataToSend = fCiph.getvalue()
            self.__socket.sendall(dataToSend)
            self.__socket.sendall('EOFX'.encode('utf-8'))
            response_data = b''
            while True:
                chunk = self.__socket.recv(self.__buffer_size)
                if not chunk:
                    print("Server closed the connection.")
                    break

                response_data += chunk
                if b'EOFX' in chunk:
                    response_data = response_data.replace(b'EOFX', b'')
                    break
            fIn = io.BytesIO(response_data)
            fDec = io.BytesIO()
            pyAesCrypt.decryptStream(fIn, fDec, self.__password, self.__buffer_size, len(response_data))
            decrypted_data = fDec.getvalue().decode('utf-8')

            self.__response = json.loads(decrypted_data)
            print(self.__response)
            return self.__response

        except socket.error as e:
            print(f"Socket error during communication: {e}")
        except ValueError as e:
            print(f"Decryption error: {e}")

    """
    Name: register_page
    Parameters: page_class: Class
    Returns: None
    Purpose: Takes a page and adds it to the tkinter frame 
    where it can be called and raised to the top
    """
    def register_page(self, page_class):
        self.__page_name = page_class.__name__
        self.__frame = page_class(parent=self, controller=self)
        self.frames[self.__page_name] = self.__frame
        self.__frame.grid(row=0, column=0, sticky="nsew")

    """
    Name: show_frame
    Parameters: page_name: String
    Returns: None
    Purpose: Raises the needed frame to the top so it can be seen to the user
    """
    def show_frame(self, page_name):
        if page_name not in self.frames:
            self.__page_class = self.__page_dict[page_name]
            self.register_page(self.__page_class)

        self.__frame = self.frames[page_name]
        self.__frame.tkraise()

        self.__current_frame = self.__frame

    """
    Name: go_to
    Parameters: page_name: String
    Returns: None
    Purpose: Pushes the page onto a stack and calls the 
    show_frame to raise the window to the top
    """
    def go_to(self, page_name):
        self.__current_frame = self.get_current_frame()
        if self.__current_frame and self.__current_frame.__class__.__name__ != page_name:
            self.__history_stack.push(self.__current_frame.__class__.__name__)
            self.__forward_stack = Stack()

        self.show_frame(page_name)

    """
    Name: go_back
    Parameters: None
    Returns: None 
    Purpose: Pops the stack for the most recent page and 
    raises it to the top to be seen by the user
    """
    def go_back(self):
        if not self.__history_stack.isempty():
            previous_page = self.__history_stack.pop()
            self.__current_frame = self.get_current_frame()
            if self.__current_frame:
                self.__forward_stack.push(self.__current_frame.__class__.__name__)
            self.show_frame(previous_page)

    """
    Name: go_forward
    Parameters: None
    Returns: None
    Purpose: Pops the forward stack for the page we 
    left when going back, thus raising it 
    """
    def go_forward(self):
        if not self.__forward_stack.isempty():
            next_page = self.__forward_stack.pop()
            self.__current_frame = self.get_current_frame()
            if self.__current_frame:
                self.__history_stack.push(self.__current_frame.__class__.__name__)
            self.show_frame(next_page)

    """
    Name: get_current_frame
    Parameters: None
    Returns: current_frame
    Purpose: Getter for the current frame
    """
    def get_current_frame(self):
        return self.__current_frame


app = MyApp()
app.mainloop()
