import socket
import os
def send_file(socket, filename):
    with open(filename, "rb") as f:
        file_data = f.read()
        socket.sendall(file_data)

def recv_file(socket, filename):
    with open(filename, "wb") as f:
        while True:
            file_data = socket.recv(1024)
            if not file_data:
                break

            f.write(file_data)

def send_listing(socket):
    listing = os.listdir()
    listing_string = "\n".join(listing)
    socket.sendall(listing_string.encode())

def recv_listing(socket):
    listing_string = socket.recv(1024).decode()
    listing = listing_string.split("\n")
    return listing

def main():
    srv_host = input("Enter the server host: ")
    server_port = int(input("Enter the server port: "))
    command_req = input("please give the wanted command type [get, put, list]")

    if command_req == "put" or command_req == "get":
        filename = input("please give the wanted file name")

    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_sock.connect((srv_host, server_port))

    cli_sock.sendall(command_req.encode())

    if command_req == "get":
        recv_file(cli_sock, filename)
    elif command_req == "put":
        send_file(cli_sock, filename)
    elif command_req== "list":
        listing = recv_listing(cli_sock)

        print("Listing received from server:")
        for item in listing:
            print(item)

    cli_sock.close()

if __name__ == "__main__":
    main()