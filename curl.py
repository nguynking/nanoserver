from urllib.parse import urlparse
import sys
import socket

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python curl.py <url>")
        exit(1)

    url = urlparse(sys.argv[1])
    host = url.hostname
    port = url.port if url.port else 80
    path = url.path if url.path else "/"

    if host is None:
        print("Invalid URL")
        exit(1)
    if url.scheme != "http":
        print("Only HTTP is supported")
        exit(1)

    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nAccept: */*\r\nConnection: close\r\n\r\n"

    print(f"connecting to {host}")
    print(f"Sending request {request}")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(request.encode('utf-8'))
    response = b""
    while True:
        chunk = s.recv(2048)
        if not chunk:
            break
        response += chunk
    print(response.decode('utf-8'))
    s.close()