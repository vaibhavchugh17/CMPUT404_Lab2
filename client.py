import socket

BYTES = 4096
HOST = "localhost"

def get(host,port):

    request = b"GET / HTTP/1.1\nHost:" + host.encode("utf-8") + b"\n\n" #Why do we need two newlines? Because the HTTP protocol requires it. The first newline is the end of the request line, and the second newline is the end of the header section. The header section is required to be terminated by a blank line.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(request)
    sock.shutdown(socket.SHUT_WR) #shuts down the write (our sending part) of the socket
    result = sock.recv(BYTES)
    while (len(result)>0):
        print(result)
        print()
        result = sock.recv(BYTES)

    sock.close()

def main():
    get("www.google.com", 80)


main() 