import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 1000))  # Connect to the server

    while True:
        message = input("Client: ")  # Get user input
        if message == "FILE":
            client.sendall(message.encode('utf-8'))  # Send the message to the server
            file_name = input("Enter the filename to send: ")
            client.sendall(file_name.encode('utf-8'))  # Send the file name to the server
            with open(file_name, 'rb') as file:
                file_data = file.read(1024)
                while file_data:
                    client.sendall(file_data)  # Send the file data to the server
                    file_data = file.read(1024)
        else:
            client.sendall(message.encode('utf-8'))  # Send the message to the server

        reply = client.recv(1024).decode('utf-8')  # Receive the server's reply
        if reply == "FILE":
            file_name = client.recv(1024).decode('utf-8')  # Receive the file name from the server
            with open(file_name, 'wb') as file:
                file_data = client.recv(1024)  # Receive the file data from the server
                while file_data:
                    file.write(file_data)  # Write the file data to the file
                    file_data = client.recv(1024)
            print(f"Received file: {file_name}")  # Print the received file name
        else:
            print(f"Server: {reply}")  # Print the server's reply

if __name__ == "__main__":
    main()
