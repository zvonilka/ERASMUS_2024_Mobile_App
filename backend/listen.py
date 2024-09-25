import socket

def start_udp_server(host='127.0.0.1', port=8080):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    sock.bind((host, port))
    print(f"Listening on {host}:{port}...")

    while True:
        message, addr = sock.recvfrom(1024)  
        print(f"Received message from {addr}: {message.decode()}")

if __name__ == "__main__":
    start_udp_server(port=8080)  

