from peer import Peer

def main():
    host = input("Enter your host (IP address): ")
    port = int(input("Enter your port number: "))

    # Create a peer instance
    peer = Peer(host, port)
    peer.start()

    print("You can start chatting! Type your messages below:")
    
    # Add a known peer manually for testing
    while True:
        peer_address = input("Enter peer address to connect to (format: IP:PORT) or type 'done' to finish: ")
        if peer_address.lower() == 'done':
            break
        try:
            peer_ip, peer_port = peer_address.split(':')
            peer.add_peer((peer_ip, int(peer_port)))
        except ValueError:
            print("Invalid format. Please use 'IP:PORT'.")

    while True:
        message = input("Message: ")
        if message.lower() == 'exit':
            break
        peer.send_message(message)

if __name__ == "__main__":
    main()
