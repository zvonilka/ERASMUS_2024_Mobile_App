import socket
import rsa

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8080))

public_key_data = client.recv(1024)
public_key = rsa.PublicKey.load_pkcs1(public_key_data, format='PEM')

action = input("Do you want to sign up or login? (signup/login): ").strip().lower()

if action == "signup":
    client.send("signup".encode())
    
    username = input("Enter username: ")
    encrypted_username = rsa.encrypt(username.encode(), public_key)
    client.send(encrypted_username)

    password = input("Enter password: ")
    encrypted_password = rsa.encrypt(password.encode(), public_key)
    client.send(encrypted_password)

elif action == "login":
    client.send("login".encode())
    
    username = input("Enter username: ")
    encrypted_username = rsa.encrypt(username.encode(), public_key)
    client.send(encrypted_username)

    password = input("Enter password: ")
    encrypted_password = rsa.encrypt(password.encode(), public_key)
    client.send(encrypted_password)

else:
    print("Invalid action!")
    client.close()
    exit(1)

response = client.recv(1024).decode()
print(response)

client.close()
