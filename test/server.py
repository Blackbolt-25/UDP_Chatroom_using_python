import socket

def main():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to a specific IP address and port
    server_address = ('localhost', 9999)
    server_socket.bind(server_address)

    print("Chat room server is running...")

    # Loop to receive messages from clients
    while True:
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode()
        print(f"Received from {client_address}: {message}")

        # Broadcast the message to all connected clients
        for client in clients:
            server_socket.sendto(data, client)

if __name__ == "__main__":
    main()
