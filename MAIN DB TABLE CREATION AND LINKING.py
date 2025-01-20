import sqlite3

"""
Name: runsql
Parameters: sqlstring: string
Returns: List
Purpose: Executes an sql command and returns the output
"""
def runsql(sqlstring):
    conn = sqlite3.connect("main_DB.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    cursor.execute(sqlstring)
    conn.commit()
    return cursor.fetchall()


sqlstring = """
CREATE TABLE IF NOT EXISTS tblUsers (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Forname TEXT,
    Surname TEXT,
    MasterPasswordHash TEXT,
    Email TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
runsql(sqlstring)

sqlstring = """
CREATE TABLE IF NOT EXISTS tblPasswords (
    PasswordID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    WebsiteURL TEXT NOT NULL,
    WebsiteUsername TEXT NOT NULL,
    EncryptedPassword BLOB NOT NULL,
    Note TEXT NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES tblUsers(UserID) ON DELETE CASCADE
)
"""
runsql(sqlstring)

sqlstring = """
CREATE TABLE IF NOT EXISTS tblFolders (
    FolderID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    FolderName TEXT NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES tblUsers(UserID) ON DELETE CASCADE
)
"""
runsql(sqlstring)

sqlstring = """
CREATE TABLE IF NOT EXISTS tblFolderEntries (
    FolderID INTEGER NOT NULL,
    PasswordID INTEGER NOT NULL,
    PRIMARY KEY (FolderID, PasswordID),
    FOREIGN KEY (FolderID) REFERENCES tblFolders(FolderID) ON DELETE CASCADE,
    FOREIGN KEY (PasswordID) REFERENCES tblPasswords(PasswordID) ON DELETE CASCADE
)
"""
runsql(sqlstring)

sqlstring = """
CREATE TABLE IF NOT EXISTS tblAuditLog (
    LogID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    Action TEXT NOT NULL,
    TimeStamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES tblUsers(UserID) ON DELETE CASCADE
"""


