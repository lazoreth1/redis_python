import socket
import threading

import select

from app.main import handle_command


def start_server():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Started")
    server_socket = socket.create_server(("localhost", 6379))
    while True:
        sock, addr = server_socket.accept()  # wait for client
        print(f"Connected : {addr}")
        threading.Thread(handle_command(sock))
