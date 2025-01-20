import sqlite3

"""
Name: runsql
Parameters: sqlstring: string
Returns: List
Purpose: Executes an sql command and returns the output
"""


def runsql(*args):
    conn = sqlite3.connect("main_DB.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    if len(args) == 1:
        cursor.execute(args[0])
    else:
        cursor.execute(args[0], args[1])
    conn.commit()
    response = cursor.fetchall()
    conn.close()
    return response


"""
Name: password_insertion
Parameters: values: Tuple
Returns: None
Purpose: Contains and runs the sql query to insert a new password into the database
"""


def password_insertion(values: tuple):
    user_id = values[0]
    URL = values[1]
    username = values[2]
    password = values[3]
    note = values[4]
    folder_name = values[5]

    conn = sqlite3.connect("main_DB.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    sqlstring = """
    SELECT FolderID
    FROM tblFolders
    WHERE UserID = ? AND FolderName = ?
    """
    cursor.execute(sqlstring, (user_id, folder_name))
    folder_id = cursor.fetchone()
    if folder_id:
        folder_id = folder_id[0]
    else:
        raise ValueError("Folder not found for the given UserID and FolderName.")

    sqlstring = """
    INSERT INTO tblPasswords (UserID, WebsiteURL, WebsiteUsername, EncryptedPassword, Note)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(sqlstring, (user_id, URL, username, password, note))

    password_id = cursor.lastrowid

    sqlstring = """
    INSERT INTO tblFolderEntries (FolderID, PasswordID)
    VALUES (?, ?)
    """
    cursor.execute(sqlstring, (folder_id, password_id))

    conn.commit()
    conn.close()


"""
Name: create_user
Parameters: values: Tuple
Returns: None
Purpose: Contains and runs the sql query to create a new user
"""


def create_user(values: tuple):
    sqlstring = """
    INSERT INTO tblUsers (Forname, Surname, MasterPasswordHash, Email)
    VALUES (?,?,?,?)
    """
    runsql(sqlstring, values)


"""
Name: login_query
Parameters: values: Tuple
Returns: List
Purpose: Contains and runs the sql query to get the hash of the master password for comparison
"""


def login_query(values: tuple):
    sqlstring = """
    SELECT MasterPasswordHash
    FROM tblUsers
    WHERE Email = ?
    """
    return runsql(sqlstring, values)


"""
Name: change_master_password
Parameters: values: Tuple
Returns: List
Purpose: Contains and runs the sql query to change the master password
"""


def change_master_password(values: tuple):
    sqlstring = """
    UPDATE tblUser
    SET MasterPasswordHash = ?
    WHERE UserID = ?
    """
    return runsql(sqlstring, values)


"""
Name: retrieve_user_id
Parameters: values: Tuple
Returns: user_id: List
Purpose: Contains and runs the sql query to get the users unique identifier
"""


def retrieve_user_id(values: tuple):
    sqlstring = """
    SELECT UserID
    FROM tblUsers
    WHERE Email = ? AND MasterPasswordHash = ?
    """
    return runsql(sqlstring, values)


"""
Name: email_in_use 
Parameters: values: Tuple
Returns: result: List
Purpose: Contains and runs the sql query to check if an email is in the database
"""


def email_in_use(values: tuple):
    sqlstring = """
        SELECT 1
        FROM tblUsers
        WHERE Email = ?
    """
    result = runsql(sqlstring, values)
    return result


"""
Name: retrieve_passwords
Parameters: values: Tuple
Returns: List
Purpose: Contains and runs the sql query to get all the users passwords
"""


def retrieve_passwords(values: tuple):
    sqlstring = """
            SELECT EncryptedPassword 
            FROM tblPasswords
            WHERE userID = ?
            """
    return runsql(sqlstring, values)


"""
Name: create_folder
Parameters: values: Tuple
Returns: None
Purpose: Contains and runs the sql query to create a new folder for the user
"""


def create_folder(values: tuple):
    sqlstring = """
    INSERT INTO tblFolders (UserID, FolderName)
    VALUES (?, ?)
    """
    runsql(sqlstring, values)


"""
Name: get_folders
Parameters: values: Tuple
Returns: List
Purpose: Contains and runs the sql query to retrieve all the users folders
"""


def get_folders(values: tuple):
    sqlstring = """
    SELECT FolderName
    From tblFolders
    WHERE userID = ?
    """
    return runsql(sqlstring, values)


"""
Name: get_passwords_wfolders
Parameters: values: Tuple
Returns: List
Purpose: Returns the passwords with their folders
"""


def get_passwords_wfolders(values: tuple):
    sqlstring = """
    SELECT tblPasswords.PasswordID, tblPasswords.WebsiteURL, tblPasswords.WebsiteUsername, tblPasswords.EncryptedPassword, tblPasswords.Note, tblFolders.FolderName
        FROM tblPasswords
        JOIN tblFolderEntries ON tblPasswords.PasswordID = tblFolderEntries.PasswordID
        JOIN tblFolders ON tblFolderEntries.FolderID = tblFolders.FolderID
        WHERE tblPasswords.UserID = ?
        ORDER BY tblFolders.FolderName, tblPasswords.WebsiteURL;
    """
    return runsql(sqlstring, values)

def change_master_password_forgot(values: tuple):
    sqlstring = """
    UPDATE tblUsers
    SET MasterPasswordHash = ?
    WHERE Email = ?
    """
    runsql(sqlstring, values)
