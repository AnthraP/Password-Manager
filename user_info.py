"""
Name: UserInfo
Purpose: Holds the user id for the user which can be changed and retrieved when needed
"""
class UserInfo:
    _instance = None

    """
    Name: __new__
    Parameters: args
    Returns: None | Boolean
    Purpose: Checks if there is currently an instance of the 
    userinfo and sets the the user id variable to none if there isnt
    """

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserInfo, cls).__new__(cls, *args, **kwargs)
            cls._instance.__user_id = None
        return cls._instance

    """
    Name: set_user_id
    Parameters: user_id: Integer
    Returns: None
    Purpose: Setter for the user ID
    """

    def set_user_id(self, user_id):
        self.__user_id = user_id

    """
    Name: get_user_id
    Parameters: None
    Returns: user_id: Integer
    Purpose: Getter for the user ID
    """

    def get_user_id(self):
        return self.__user_id

