import socket
import json
import io
import pyAesCrypt
import sql_queries
import hashlib
import requests

password = "8^Ri%9B0aqtB"
buffer_size = 1024

HOST = "127.0.0.1"
PORT = 58868

"""
Name: process_command
Parameters: packet: Dictionary
Returns: response: Dictionary
Purpose: Takes the query sent by the client and 
responds with the correct answer
"""

def process_command(packet: dict):
    print("THIS THE FIRE SHIIII", packet)
    if "LOGIN" in packet:
        packet = packet["LOGIN"]
        email = packet[0]
        password_hash = packet[1]
        stored_hash = sql_queries.login_query((email,))[0][0]
        print("stored", stored_hash)
        if password_hash == stored_hash:
            response = {"Reply": True}
        else:
            response = {"Reply": False}

    elif "INSERT" in packet:
        sql_queries.password_insertion(packet.get("INSERT"))
        response = {"Reply": "Completed"}

    elif "SIGN_UP" in packet:
        sql_queries.create_user(packet.get("SIGN_UP"))
        response = {"Reply": "Completed"}

    elif "GET_USER_ID" in packet:
        response = sql_queries.retrieve_user_id(packet.get("GET_USER_ID"))[0][0]
        print(response)
        if response:
            response = {"Reply": response}
        else:
            response = {"Reply": "No User ID"}

    elif "USED_EMAIL" in packet:
        response = (packet["USED_EMAIL"][0],)
        print(response)
        response = sql_queries.email_in_use(response)
        print(response, "dddjj")
        response = {"Reply": bool(response)}

    elif "GET_PASSWORDS" in packet:
        response = sql_queries.retrieve_passwords(packet.get("GET_PASSWORDS"))
        if response:
            response = {"Reply": response}
        else:
            response = {"Reply": "No passwords found"}

    elif "CHANGE_MASTER" in packet:
        sql_queries.change_master_password(packet.get("CHANGE_MASTER"))
        response = {"Reply": "Completed"}

    elif "API_BREACHED_PASSWORD" in packet:
        user_id = packet.get("API_BREACHED_PASSWORD")
        passwords = sql_queries.retrieve_passwords((user_id,))
        if not passwords:
            return {"Reply": "No passwords found"}

        data_at_compromise = []

        for password_tuple in passwords:
            password = password_tuple[0]
            print("This the password", password)
            if isinstance(password, bytes):
                password = password.decode('utf-8')

            hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

            try:
                response = requests.get(f"https://api.pwnedpasswords.com/range/{hashed_password[:5]}")
                response.raise_for_status()
            except requests.RequestException as e:
                return {"Reply": f"Error contacting breach API: {str(e)}"}

            hashes = (line.split(':') for line in response.text.splitlines())
            for h, count in hashes:
                if h == hashed_password[5:]:
                    data_at_compromise.append(f"Password: {password} | Breach Count: {int(count)}")
                    break

        if not data_at_compromise:
            return {"Reply": "No passwords found"}
        else:
            return {"Reply": data_at_compromise}

    elif "CREATE_FOLDER" in packet:
        sql_queries.create_folder(packet.get("CREATE_FOLDER"))
        response = {"Reply": "Completed"}

    elif "GET_FOLDERS" in packet:
        data = packet.get("GET_FOLDERS")
        data = (data,)
        response = sql_queries.get_folders(data)
        print(response)
        if response:
            response = [t[0] for t in response]
            response = {"Reply": response}
        else:
            response = {"Reply": "No folders found"}

    elif "GET_PASSWORDS_WFOLDERS" in packet:
        response = sql_queries.get_passwords_wfolders(packet.get("GET_PASSWORDS_WFOLDERS"))
        print("amam", response)
        if response:
            response = {"Reply": response}
        else:
            response = {"Reply": "No passwords found"}

    elif "CHANGE_MASTER_PASSWORD_FORGOT" in packet:
        response = packet.get("CHANGE_MASTER_PASSWORD_FORGOT")
        print(response, "ff")
        sql_queries.change_master_password_forgot(response)
        response = {"Reply": "Completed"}

    else:
        response = {"Error": "Unknown command"}


    print(response)
    return response


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            try:
                while True:
                    data = b""
                    while True:
                        chunk = conn.recv(buffer_size)
                        if not chunk:
                            print("Client closed connection.")
                            break
                        data += chunk
                        if b'EOFX' in chunk:
                            data = data.replace(b'EOFX', b'')
                            break

                    if not data:
                        break

                    fIn = io.BytesIO(data)
                    fDec = io.BytesIO()
                    pyAesCrypt.decryptStream(fIn, fDec, password, buffer_size, len(data))
                    decrypted_data = fDec.getvalue().decode('utf-8')

                    packet = json.loads(decrypted_data)
                    print("Received packet:", packet)

                    response = json.dumps(process_command(packet)).encode('utf-8')

                    fIn = io.BytesIO(response)
                    fCiph = io.BytesIO()
                    pyAesCrypt.encryptStream(fIn, fCiph, password, buffer_size)
                    encrypted_reply = fCiph.getvalue()

                    conn.sendall(encrypted_reply)
                    conn.sendall(b'EOFX') 

            except Exception as e:
                print(f"Error during communication: {e}")



