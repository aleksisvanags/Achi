# AchiServer
# Aleksis Vanags
# 26/08/2023 - 27/08/2023

import socket
import threading
import json
import AchiLogic
import AchiCommonVariables

print("[SERVER] Server is starting...")

HEADER = 12
FORMAT = "utf-8"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)

connections = []

def HandleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connections.append(conn)
    conn.send(json.dumps(AchiCommonVariables.grid).encode(FORMAT))

    while True:
        try:
            msg = conn.recv(HEADER).decode(FORMAT)

            AchiLogic.Process(msg)

            grid = json.dumps(AchiCommonVariables.grid).encode(FORMAT)

            for connection in connections:
                connection.send(grid)
        except ConnectionResetError:
            print(f"[{addr}] Disconnected")

            break

    connections.remove(conn)
    conn.close()

def main():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=HandleClient, args=(conn, addr))

        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
