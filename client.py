import os
import socket
import sys
import threading

# server config
HOST = '0.0.0.0'  
PORT = 8080    

# to continuously receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(4096).decode()
            if message:
                print(message)
            else:
                break
        except:
            print("Connection closed by the server.")
            break

def application(client_socket):
    while True:
        request = input()

        if request.lower() == "exit()":
            client_socket.sendall(request.encode())
            break
        
        client_socket.sendall(request.encode())

if __name__ == "__main__":
    try: 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))

            receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
            receive_thread.start()

            application(client_socket)
    except KeyboardInterrupt:
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)