from peer import Peer
import socket

def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))  
    return sock.getsockname()[0]

def main():
    host = get_local_ip()  
    port = 8080 

    peer = Peer(host, port)
    peer.start()

    peer_address = "127.0.0.1:8080"

    peer_ip, peer_port = peer_address.split(':')
    peer.add_peer((peer_ip, int(peer_port)))
        

    while True:
        message = input("Message: ")
        if message.lower() == 'exit':
            peer.close()  # Ensure the socket is closed on exit
            break
        if message.startswith("to "):
            # Send message to a specific peer
            _, peer_address, msg = message.split(" ", 2)
            try:
                peer_ip, peer_port = peer_address.split(':')
                peer.send_message(msg, (peer_ip, int(peer_port)))
            except ValueError:
                print("Invalid peer address format. Use 'to IP:PORT message'.")
        else:
            peer.send_message(message)  # Broadcast

if __name__ == "__main__":
    main()

