import os
import socket
import sys
import threading

HOST = '0.0.0.0'
PORT = 8080

clients = [] 
nick = {}  # conn to nick map

# broadcast message to all connected clients
def broadcast(message, sender_conn=None):
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message)
            except:
                client.close()
                clients.remove(client) 

def handle_client(conn, addr):
    print(f"OPENED CONNECTION: {addr} (ACTIVE {len(clients)})")
    conn.sendall(f"You are connected to the chat as {nick[conn]}.".encode())
    conn.sendall("\nCommands:\n/help            - See all available commands\n/nick <nickname> - Change your nickname\n/exit            - Leave the chat\n".encode())

    broadcast(f"{nick[conn]} joined the chat".encode())

    while True:
        try:
            # receive data from the client
            request = conn.recv(1024).decode()

            if not request:
                    break  # gandle disconnection

            elif request.startswith("/help"):
                conn.sendall("Commands:\n/nick <nickname> - Change your nickname\n/exit - Leave the chat".encode())

            elif request.startswith("/nick"):
                nickname = request.split("/nick ")[1]
                nick[conn] = nickname
                conn.sendall(f"Your nickname has been changed to {nickname}".encode())
                print(f"CHANGED NICK: {addr} -> {nickname}")

            elif request.lower() == "/exit":
                broadcast(f"{nick[conn]} left the chat.".encode(), conn)
                break
            
            else:
                print(f"SENT MESSAGE: {addr} -> {request}")            
                broadcast(f"{nick[conn]}: {request}".encode(), conn)

        except ConnectionResetError:
            break

    conn.close()
    clients.remove(conn)
    print(f"CLOSED CONNECTION: {addr} (ACTIVE {len(clients)})")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allow reuse of the address, multiple clients per IP
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            clients.append(conn)
            nick[conn] = addr
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)