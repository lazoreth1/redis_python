import socket

s = socket.socket()
host = 'localhost' # needs to be in quote
port = 6379
s.connect((host, port))
# print(s.recv(1024))
s.send(b"PING")
print("the message has been sent")
data = s.recv(1024)
print(data.decode())