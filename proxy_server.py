#Client connects to proxy server, proxy server connects to a different server for eg google.com. 
#google.com sends the response back to the proxy server and then the proxy server sends the response back to the client.

import socket
from threading import Thread

BYTES = 4096
PROXY_SERVER_HOST = "localhost"
PROXY_SERVER_PORT = 8080

def send_request(host, port, request): #Now this proxy server is a client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #Sending data to google.com
        sock.connect((host, port))
        sock.send(request)
        sock.shutdown(socket.SHUT_WR)

        #Receiving data from google.com
        response = sock.recv(BYTES)
        result = b""+response
        while (len(response)>0):
            response = sock.recv(BYTES)
            result += response
            
        return result

def handle_connection(conn, addr):
    with conn:
        print("Connected by", addr)
        request = b""
        while True:
            data = conn.recv(BYTES)
            if not data: break
            print(data)
            request += data

        response = send_request("www.google.com", 80, request) #Proxy_server is this server which then sends another request to get stuff from google.com and then sends it back to the client.
        conn.sendall(response)

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.listen(2)
        conn, addr = sock.accept()
        handle_connection(conn, addr)

def multithreaded_server():
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((PROXY_SERVER_HOST,PROXY_SERVER_PORT))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.listen(2)
        
        while True:
            conn, addr = sock.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

#server()
multithreaded_server()