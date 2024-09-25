import sqlite3
import hashlib
import socket
import threading
import rsa

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8000))
server.listen()

(public_key, private_key) = rsa.newkeys(512)

def create_database():
    with sqlite3.connect("userdata.db") as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS userdata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

def decrypt_data(encrypted_data):
    """Decrypt incoming data using the private RSA key."""
    return rsa.decrypt(encrypted_data, private_key).decode()

def hash_password(password):
    """Hash a plaintext password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(c, username, password):
    """Sign up a new user, handle username uniqueness."""
    hashed_password = hash_password(password)
    
    with sqlite3.connect("userdata.db") as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            c.send("Sign up successful!".encode())
        except sqlite3.IntegrityError:
            c.send("Username already exists!".encode())

def login_user(c, username, password):
    """Log in a user by verifying username and password."""
    hashed_password = hash_password(password)
    
    with sqlite3.connect("userdata.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))
        
        if cur.fetchone():
            c.send("Login successful!".encode())
        else:
            c.send("Login failed!".encode())

def search_user(c, search_term):
    """Search for users by username (partial match)."""
    with sqlite3.connect("userdata.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username FROM userdata WHERE username LIKE ?", ('%' + search_term + '%',))
        results = cur.fetchall()

    if results:
        response = "\n".join([f"ID: {row[0]}, Username: {row[1]}" for row in results])
    else:
        response = "No users found with that username."

    c.send(response.encode())

def handle_connection(c):
    # Send public key
    c.send(public_key.save_pkcs1(format='PEM'))

    command = c.recv(1024).decode()

    if command == "signup":
        username_length = int.from_bytes(c.recv(4), byteorder='big')  # Length of username
        encrypted_username = c.recv(username_length)
        username = decrypt_data(encrypted_username)

        password_length = int.from_bytes(c.recv(4), byteorder='big')  # Length of password
        encrypted_password = c.recv(password_length)
        password = decrypt_data(encrypted_password)

        signup_user(c, username, password)

    elif command == "login":
        username_length = int.from_bytes(c.recv(4), byteorder='big')  # Length of username
        encrypted_username = c.recv(username_length)
        username = decrypt_data(encrypted_username)

        password_length = int.from_bytes(c.recv(4), byteorder='big')  # Length of password
        encrypted_password = c.recv(password_length)
        password = decrypt_data(encrypted_password)

        login_user(c, username, password)

    elif command == "search":
        search_term_length = int.from_bytes(c.recv(4), byteorder='big')  # Length of search term
        encrypted_search_term = c.recv(search_term_length)
        search_term = decrypt_data(encrypted_search_term)
        search_user(c, search_term)

    else:
        c.send("Invalid command!".encode())

if __name__ == "__main__":
    create_database()
    
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_connection, args=(client,)).start()