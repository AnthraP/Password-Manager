"""
Name: Stack
Purpose: A static stack data structure used to hold page names
"""
class Stack:

    """
    Name: __init___
    Parameters: None
    Returns: None
    Purpose: initialises the default variables for the stack
    """
    def __init__(self):
        self.__data = [None, None, None, None, None, None, None, None, None, None]
        self.__pointer = -1

    """
    Name: push
    Parameters: newdata: String
    Returns: String
    Purpose: Adds new data to the stack 
    """

    def push(self, newdata):
        if self.isfull():
            return "There is no room"
        else:
            self.__pointer += 1
            self.__data[self.__pointer] = newdata

    """
    Name: pop
    Parameters: None
    Returns: String | popped_data: String
    Purpose: Removes the data from the top of the stack and returns it
    """

    def pop(self):
        if self.isempty():
            return "The stack is full, cannot remove None"
        else:
            self.__popped_data = self.__data[self.__pointer]
            self.__data[self.__pointer] = None
            self.__pointer -= 1
            return self.__popped_data

    """
    Name: peek
    Parameters: None
    Returns: String
    Purpose: Returns the values at the top of the stack
    """

    def peek(self):
        return self.__data[self.__pointer]

    """
    Name: isempty
    Parameters: None
    Returns: Boolean
    Purpose: Checks if the stack has no values in it 
    and returns the appropriate boolean values
    """

    def isempty(self):
        if self.__pointer <= -1:
            return True
        else:
            return False

    """
    Name: isfull
    Parameters: None
    Returns: Boolean
    Purpose: Checks if the stack is full
    and returns the appropriate boolean values
    """

    def isfull(self):
        if self.__pointer >= 9:
            return True
        else:
            return False

    """
    Name: spaces_free
    Parameters: None
    Returns: String
    Purpose: Returns how many spaces are in the stack
    """

    def spaces_free(self):
        spaces = 9 - self.__pointer
        return f"{spaces} spaces free"


