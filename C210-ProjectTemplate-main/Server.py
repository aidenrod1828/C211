import socket
from  threading import Thread

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


IP_ADDRESS = '127.0.0.1'
PORT = 8050
SERVER = None
BUFFER_SIZE = 4096

clients = {}

def setup():
    print("\n\t\t\t\t\t\LIP MESSENGER\n")
    global PORT
    global IP_ADDRESS
    global SERVER
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind(IP_ADDRESS, PORT)
    SERVER.listen(100)
    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")
    acceptConnections()

def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr=SERVER.accept()
        client_name = client.recv(4056).decode().lower()
        client[client_name] = {
            "client":client,
            "address":addr,
            "connected_with":"",
            "file_name":"",
            "file_size":4069
            }
        print(f"Connection established with {client_name} : {addr}")

        thread = Thread(target=handleClient, args=(client, client_name,))
        thread.start()

def ftp():
    global IP_ADDRESS

    authorizer = DummyAuthorizer()
    authorizer.add_user("lftpd","lftpd", ".", perm="elradfmw")

    handler = FTPServer
    handler.authorizer = authorizer

    ftp_server = FTPServer((IP_ADDRESS, 21), handler)
    ftp_server.serve_forever()

setup_thread=Thread(target=setup)
setup_thread.start()
