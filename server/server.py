import sqlite3
import hashlib
import socket
import threading
import rsa

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8080))
server.listen()

(public_key, private_key) = rsa.newkeys(512)

def create_database():
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS userdata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_database()

def handle_connection(c):
    c.send(public_key.save_pkcs1(format='PEM'))

    command = c.recv(1024).decode()

    if command == "signup":
        encrypted_username = c.recv(1024)
        username = rsa.decrypt(encrypted_username, private_key).decode()

        encrypted_password = c.recv(1024)
        password = rsa.decrypt(encrypted_password, private_key).decode()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            c.send("Sign up successful!".encode())
        except sqlite3.IntegrityError:
            c.send("Username already exists!".encode())
        finally:
            conn.close()

    elif command == "login":
        encrypted_username = c.recv(1024)
        username = rsa.decrypt(encrypted_username, private_key).decode()

        encrypted_password = c.recv(1024)
        password = rsa.decrypt(encrypted_password, private_key).decode()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))

        if cur.fetchall():
            c.send("Login successful!".encode())
        else:
            c.send("Login failed!".encode())
        
        conn.close()  
    else:
        c.send("Invalid command!".encode())

    # c.close()  
while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()
