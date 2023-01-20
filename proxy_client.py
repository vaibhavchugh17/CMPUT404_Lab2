import socket

BYTES = 4096

def get(host,port):

    request = b"GET / HTTP/1.1\nHost: www.google.com\n\n"  #This will go to proxy_server which will then send this over to google.com
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.send(request)
        sock.shutdown(socket.SHUT_WR)

        print("Waiting for response...")
        response = sock.recv(BYTES)
        result = b""+response
        while (len(response)>0):
            response = sock.recv(BYTES)
            result += response
        
        return result

def main():
    print(get("127.0.0.1", 8080)) #proxy server


main() 
