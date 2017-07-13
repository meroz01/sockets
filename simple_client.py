import socket


def init():
    s = socket.socket()
    host = socket.gethostname()
    port = 7070

    s.connect((host, port))
    print(s.recv(1024).decode('utf-8'))
    s.close()


if __name__ == '__main__':
    init()

