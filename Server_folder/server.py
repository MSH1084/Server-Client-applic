import socket
import os
import sys


def send_file(socket, filename):
    with open(filename, "rb") as f:
        file_data = f.read() 
        socket.sendall(file_data) 

def recv_file(socket, filename): 
        file_path = os.path.join(filename)
        with open(file_path, "wb") as f:
            while True:
                file_data = socket.recv(1024)
                if not file_data:
                    break
                f.write(file_data) 

def send_listing(socket):
    listing = os.listdir() 
    listing_string = " ".join(listing)
    socket.sendall(listing_string.encode()) 

def recv_listing (socket): 
    listing_string = socket.recv(1024).decode()
    listing = listing_string.split("\n")
    return listing



def manage_get_request(socket, client_addr):
    filename = socket.recv(1024).decode()

    if not os.path.exists(filename):
        socket.sendall(b"The file does not exist.")
        return

    send_file(socket, filename)

def handle_put_request(socket, client_addr): 
    filename = socket.recv(1024).decode() 

    if os.path.exists (filename): 
        socket.sendall(b"The file already exists.")
        return

    recv_file(socket, filename) 

def handle_list_request(socket, client_addr): 
    listing = os.listdir() 
    listing_string = " ".join(listing) 
    socket.sendall(listing_string.encode()) 

    print("List sent to client: {}.".format(listing))


def main():
    port = int(sys.argv[1])
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    srv_sock.bind (("0.0.0.0", port))
    

    srv_sock.listen(15)

    print("the server is on port {}.".format(port))

    while True:
        cli_sock, cli_addr = srv_sock.accept()
        command_wanted = cli_sock.recv(1024).decode()
        if command_wanted == "get":
            manage_get_request(cli_sock, cli_addr)
        elif command_wanted == "put":
            handle_put_request(cli_sock, cli_addr)
        elif command_wanted == "list":
            handle_list_request(cli_sock, cli_addr)
        else:
            print("Invalid request type: {}".format(command_wanted))

        cli_sock.close()


if __name__ == "__main__":
    main()