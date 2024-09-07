import socket  # noqa: F401
from dataclasses import dataclass


def handle_set(data):
    return "SET command processed"


def handle_unset(data):
    return "UNSET command processed"


def handle_ping(data):
    print("ping_func")
    return "+PONG\r\n"


commands = {
    'SET': handle_set,
    'UNSET': handle_unset,
    'PING': handle_ping,
}


class Type:
    pass


@dataclass
class Request:
    command: str
    type: Type
    data: list


@dataclass
class Array(Type):
    array_len: int


def parse_type(s: str):
    t = None
    match s[0]:
        case "*":
            t = Array(array_len=int(s[1]))
    return t


def parse_command(s: str):
    print(f"command: {s}")
    match s:
        case "PING":
            return "PING"


def parse_request(data: bytes):
    r = data.decode().split()
    print(r)
    request_type = parse_type(r[0])
    r = r[1:]
    command = parse_command(r[1])
    r = r[2:]
    req = Request(command=command, type=request_type, data=r)
    print(req)
    match req.command:
        case "PING":
            return "+PONG"
    # match req.type:
    #     case Array():
    #         for i in range(1, len(r), 2):
    #             l = r[i - 1]
    #             word_len = int(l[1:])
    #             word = r[i]
    #             print(f"Word: {word}, Len: {word_len}")


def handle_command(sock):
    try:
        while True:
            response = None
            data = sock.recv(1024)
            if not data:
                break
            print(f"Got: {data.decode()}")
            response = parse_request(data) + "\r\n"
            print("parsed")
            sock.send(response.encode())
            print("sent")
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
