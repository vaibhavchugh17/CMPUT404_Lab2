#Creating an echo server
import socket
from threading import Thread

BYTES = 4096
HOST = "127.0.0.1" #localhost is a DNS name that resolves to our own IP address.
PORT = 8080

def handle_connection(conn, addr):
    with conn: #with statement automatically closes the connection when we're done with it.
        print("Connected by", addr)
        while True:
            data = conn.recv(BYTES)
            if not data: break
            print(data)
            conn.sendall(data) #sendall() is like send(), but it will keep sending data until all of it has been sent. send() will only send as much data as the OS can handle at the time.


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #with statement automatically closes the socket when we're done with it.
        sock.bind((HOST, PORT))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #This line allows us to reuse the same port number over and over again. Without it, we'd have to wait for the OS to release the port before we could reuse it.
        sock.listen()
        conn, addr = sock.accept() #accept() blocks until a client connects to the server. conn is the connection that was made (a socket that was made by sock.accept i.e. server socket that is connected to our client now) and the addr is the address that it came from
        handle_connection(conn, addr)

def multi_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.listen(2)
        
        while True:
            conn, addr = sock.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

#server()
multi_threaded_server()