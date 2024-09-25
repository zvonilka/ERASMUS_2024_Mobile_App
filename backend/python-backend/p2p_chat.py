import socket
import threading

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []

    def start(self):
        # Start listening for incoming connections in a new thread
        threading.Thread(target=self.listen_for_connections, daemon=True).start()

    def listen_for_connections(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Listening on {self.host}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                print(f"Connection from {addr}")
                threading.Thread(target=self.handle_peer, args=(client_socket,)).start()

    def handle_peer(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"Received message: {message}")
                else:
                    break
            except:
                break
        client_socket.close()

    def add_peer(self, peer_address):
        self.peers.append(peer_address)

    def send_message(self, message):
        for peer in self.peers:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.connect(peer)
                    sock.send(message.encode())
                except Exception as e:
                    print(f"Could not send message to {peer}: {e}")

