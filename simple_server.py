import socket


def init():
    s = socket.socket()
    host = socket.gethostname()
    port = 7070
    s.bind((host, port))
    print('Connecting to {} at port {}'.format(host, port))

    s.listen(5)
    while True:
        c, addr = s.accept()
        print('Got connection from {}'.format(addr))
        c.send(b'Connection was established!')
        c.close()


if __name__ == '__main__':
    init()
