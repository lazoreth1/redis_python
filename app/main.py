import socket  # noqa: F401
from dataclasses import dataclass

from app.srv import start_server


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
        case "ECHO":
            return "ECHO"


def parse_request(data: bytes):
    r = data.decode().split()
    print(r)
    request_type = parse_type(r[0])
    r = r[1:]
    command = parse_command(r[1])
    if not len(r) == 2:
        r = r[2:]
    else:
        r = list()
    req = Request(command=command, type=request_type, data=r)
    print(req)
    ret_string = None
    match req.command:
        case "PING":
            ret_string = "+PONG"
        case "ECHO":
            if not req.data:
                return "-ERR: Invalid Command"
    match req.type:
        case Array():
            arr_str = list()
            for i in range(1, len(r), 2):
                l = r[i - 1]
                word_len = int(l[1:])
                word = r[i]
                print(f"Word: {word}, Len: {word_len}")
                arr_str.append(word)
            ret_string = "+" + " ".join(arr_str)
    print(f"ret string: {ret_string}")
    return ret_string


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


if __name__ == "__main__":
    start_server()
