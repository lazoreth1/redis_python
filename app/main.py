import socket  # noqa: F401


def handle_set(data):
    return "SET command processed"


def handle_unset(data):
    return "UNSET command processed"


def handle_ping(data):
    return "+PONG\r\n"


commands = {
    'SET': handle_set,
    'UNSET': handle_unset,
    'PING': handle_ping,
}


def handle_command(sock):
    try:
        while True:
            response = None
            data = sock.recv(1024)
            if not data:
                break
            command = data.decode().strip().split()[0]
            command_func = commands.get(command)
            if not command_func:
                response = "Unknown command"
            response = command_func(data)
            sock.send(response.encode())
            print(data)
    except ConnectionResetError:
        print("Connection closed")
        return


def start_server():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Started")
    server_socket = socket.create_server(("localhost", 6379))
    while True:
        sock, addr = server_socket.accept()  # wait for client
        print(f"Connected : {addr}")
        handle_command(sock)


if __name__ == "__main__":
    start_server()
