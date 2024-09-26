import sqlite3
import hashlib
import asyncio
import websockets
import rsa

# Generate public and private keys
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

async def signup_user(websocket, username, password):
    """Sign up a new user, handle username uniqueness."""
    hashed_password = hash_password(password)
    with sqlite3.connect("userdata.db") as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            await websocket.send("Sign up successful!")
        except sqlite3.IntegrityError:
            await websocket.send("Username already exists!")

async def login_user(websocket, username, password):
    """Log in a user by verifying username and password."""
    hashed_password = hash_password(password)
    with sqlite3.connect("userdata.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))
        if cur.fetchone():
            await websocket.send("Login successful!")
        else:
            await websocket.send("Login failed!")

async def search_user(websocket, search_term):
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
        encrypted_username = await websocket.recv()
        username = decrypt_data(encrypted_username)

        encrypted_password = await websocket.recv()
        password = decrypt_data(encrypted_password)

        await signup_user(websocket, username, password)

    elif command == "login":
        encrypted_username = await websocket.recv()
        username = decrypt_data(encrypted_username)

        encrypted_password = await websocket.recv()
        password = decrypt_data(encrypted_password)

        await login_user(websocket, username, password)

    elif command == "search":
        encrypted_search_term = await websocket.recv()
        search_term = decrypt_data(encrypted_search_term)
        await search_user(websocket, search_term)

    else:
        await websocket.send("Invalid command!")

if __name__ == "__main__":
    create_database()
    start_server = websockets.serve(handle_connection, "localhost", 8000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

