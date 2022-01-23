#!/usr/bin/env python3
import argparse
import socket


options = argparse.ArgumentParser()
options.add_argument("path", help="The HTTP path to put in the HTTP request.")
address_group = options.add_mutually_exclusive_group(required=True)
address_group.add_argument("--tcp", help="The target TCP address", type=lambda s: s.split(":"))
address_group.add_argument("--uds", help="The target Unix Domain Socket address", type=str)
options.add_argument("--action", choices=["wait_close", "close_nowait"], default="wait_close", type=str,
                     help="The action to perform - 'wait_close' to wait for the response before closing, "
                          "'close_nowait' to close without waiting for the response")


if __name__ == '__main__':
    arguments = options.parse_args()

    path = arguments.path.lstrip("/")
    if arguments.tcp:
        address = arguments.tcp
        address_family = socket.AF_INET
    else:
        address = arguments.uds
        address_family = socket.AF_UNIX

    http_request_bytes = f"""
GET /{path} HTTP/1.1
Accept: */*
Host: localhost

""".lstrip().replace("\n", "\r\n").encode("utf8")

    connection = socket.socket(address_family, socket.SOCK_STREAM)
    connection.connect(address)
    connection.sendall(http_request_bytes)

    if arguments.action == "wait_close":
        response = connection.recv(10000)
        print(response.decode("utf8"))

    connection.close()
    print("Connection closed")
