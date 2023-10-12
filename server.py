import socket
import threading

def handle_client(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')  # Receive message from client

        if message == "FILE":
            file_name = client_socket.recv(1024).decode('utf-8')  # Receive file name from client

            with open(file_name, 'wb') as file:
                file_data = client_socket.recv(1024)  # Receive file data from client

                while file_data:  # Loop until all file data is received
                    file.write(file_data) 
                    file_data = client_socket.recv(1024)

            print(f"Received file: {file_name}") 
        else:
            print(f"Client: {message}")

        reply = input("Server: ")  # Get a reply message from the server

        if reply == "FILE":
            client_socket.sendall(reply.encode('utf-8'))  # Send the reply to the client

            file_name = input("Enter the filename: ") 
            client_socket.sendall(file_name.encode('utf-8'))  # Send the file name to the client

            with open(file_name, 'rb') as file: 
                file_data = file.read(1024)

                while file_data:  # Loop until all file data is read
                    client_socket.sendall(file_data)
                    file_data = file.read(1024)
        else:
            client_socket.sendall(reply.encode('utf-8'))  # Send the reply to the client

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPv4 addressing, socket.SOCK_STREAM = TCP
    server.bind(('0.0.0.0', 1000)) # '0.0.0.0' = all available network interfaces
    server.listen(5) # 5 queued connections
    print("Server listening on port 1000")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,)) # Handling client connections in separate threads
        client_handler.start()

if __name__ == "__main__":
    main()