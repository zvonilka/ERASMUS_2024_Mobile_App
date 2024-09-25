import socket
import threading

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Use UDP for P2P
        self.socket.bind((self.host, self.port))
        self.peers = set()

    def listen_for_messages(self):
        """Listen for incoming messages from peers."""
        while True:
            try:
                message, addr = self.socket.recvfrom(1024)  # Buffer size is 1024 bytes
                print(f"\nReceived message from {addr}: {message.decode()}")
                self.peers.add(addr)  # Add peer to the list of known peers
            except Exception as e:
                print(f"Error receiving message: {e}")

    def send_message(self, message):
        """Send a message to all known peers."""
        if not self.peers:
            print("No peers available to send messages.")
            return
        for peer in self.peers:
            self.socket.sendto(message.encode(), peer)
            print(f"Sent message to {peer}: {message}")

    def start(self):
        """Start listening for incoming messages in a separate thread."""
        thread = threading.Thread(target=self.listen_for_messages)
        thread.daemon = True
        thread.start()

    def add_peer(self, peer_address):
        """Add a peer to the list of known peers."""
        self.peers.add(peer_address)
        print(f"Added peer: {peer_address}")


