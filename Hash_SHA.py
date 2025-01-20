import hashlib


"""
Name: hash_data
Parameters: data: string
Returns: hexadecimal: string
Purpose: hashes the data for the user 
"""
def hash_data(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()



