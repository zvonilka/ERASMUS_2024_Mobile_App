import socket

def start_udp_server(host='127.0.0.1', port=8080):
    """Start a UDP server that listens for messages on the specified port."""
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the specified host and port
    sock.bind((host, port))
    print(f"Listening on {host}:{port}...")

    while True:
        # Wait for a message
        message, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        print(f"Received message from {addr}: {message.decode()}")

if __name__ == "__main__":
    start_udp_server(port=8080)  # Change port as needed

