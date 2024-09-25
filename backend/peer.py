import socket
import threading

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        self.socket.bind((self.host, self.port))
        self.peers = set()

    def listen_for_messages(self):
        while True:
            try:
                message, addr = self.socket.recvfrom(1024)  
                print(f"\nReceived message from {addr}: {message.decode()}")
                self.peers.add(addr)  
            except Exception as e:
                print(f"Error receiving message: {e}")

    def send_message(self, message, target_peer=None):
        if target_peer:
            self.socket.sendto(message.encode(), target_peer)
            print(f"Sent message to {target_peer}: {message}")
        else:
                print("No peers available to send messages.")
                return
            for peer in self.peers:
                self.socket.sendto(message.encode(), peer)
                print(f"Sent message to {peer}: {message}")

    def start(self):
        thread = threading.Thread(target=self.listen_for_messages)
        thread.daemon = True
        thread.start()

    def add_peer(self, peer_address):
        self.peers.add(peer_address)
        print(f"Added peer: {peer_address}")

    def close(self):
        self.socket.close()
        print("Socket closed.")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))  
    return s.getsockname()[0]

