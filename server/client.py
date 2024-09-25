import socket
import rsa

def send_encrypted_data(client, message):
    """Helper function to encrypt and send data with length prefix."""
    encrypted_message = rsa.encrypt(message.encode('utf-8'), public_key)
    
    # Send the length of the encrypted message first
    length_bytes = len(encrypted_message).to_bytes(4, byteorder='big')
    client.send(length_bytes)  # Send the length of the encrypted message
    client.send(encrypted_message)  # Send the encrypted message

# Initialize the client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8000))

# Receive the public RSA key from the server
public_key_data = client.recv(1024)
public_key = rsa.PublicKey.load_pkcs1(public_key_data, format='PEM')

# Get the action from the user
action = input("What action do you want to perform? (signup/login/search): ").strip().lower()

if action == "signup":
    client.send("signup".encode())
    
    username = input("Enter username: ")
    send_encrypted_data(client, username)  # Send encrypted username

    password = input("Enter password: ")
    send_encrypted_data(client, password)  # Send encrypted password

elif action == "login":
    client.send("login".encode())
    
    username = input("Enter username: ")
    send_encrypted_data(client, username)  # Send encrypted username

    password = input("Enter password: ")
    send_encrypted_data(client, password)  # Send encrypted password

elif action == "search":
    client.send("search".encode())
    
    search_term = input("Enter username to search: ")
    send_encrypted_data(client, search_term)  # Send encrypted search term

else:
    print("Invalid action!")
    client.close()
    exit(1)

# Receive the server response
response = client.recv(1024).decode('utf-8')
print(response)

client.close()

