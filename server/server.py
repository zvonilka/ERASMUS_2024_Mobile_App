import sqlite3
import hashlib
import socket
import websockets
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
            await websocket.send("signup successfull")
        except sqlite3.IntegrityError:
            await websocket.send("username exists")

def login_user(c, username, password):
    """Log in a user by verifying username and password."""
    hashed_password = hash_password(password)
    
    with sqlite3.connect("userdata.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))
        if cur.fetchone():
            await websocket.send("Login successful!")
        else:
            await websocket.send("Login failed!")

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

    await websocket.send(response)

async def handle_connection(websocket, path):
    await websocket.send(public_key.save_pkcs1(format='PEM').decode())  # Send public key as PEM formatted string

    command = await websocket.recv()

    if command == "signup":
        username = await websocket.recv()
        password = await websocket.recv()

        signup_user(websocket, decrypt_data(username), decrypt_data(password))

    elif command == "login":
        username = await websocket.recv()
        password = await websocket.recv()

        login_user(websocket, decrypt_data(username), decrypt_data(password))

    elif command == "search":
        search_term = await websocket.recv()
        await search_user(websocket, decrypt_data(search_term))

    else:
        await websocket.send("Invalid command!")
        

if __name__ == "__main__":
    create_database()
    start_server = websockets.serve(handle_connection, "localhost", 8000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
