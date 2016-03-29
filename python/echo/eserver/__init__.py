#!/usr/bin/env python
__version__ = '0.0.0'

from contextlib import contextmanager

import socket


@contextmanager
def irl_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    try:
        yield s
    finally:
        s.close()


def main():
    host = ''
    port = 50000
    backlog = 5
    size = 1024
    with irl_socket(host, port) as s:
        s.listen(backlog)
        while 1:
            client, address = s.accept()
            data = client.recv(size)
            if data:
                client.send(data + b":" + data)
                client.send(b"\n")

            client.close()


def client(host, port, msg):
    BUFFER_SIZE = 1024
    MESSAGE = msg

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    s.close()
    return data

if __name__ == '__main__':
    main()
