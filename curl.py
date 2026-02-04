from urllib.parse import urlparse
import socket
import argparse
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Curl-like tool")
    parser.add_argument("url", type=str, help="URL to fetch")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    url = urlparse(args.url)
    host = url.hostname
    port = url.port if url.port else 80
    path = url.path if url.path else "/"

    if host is None:
        print("Invalid URL")
        exit(1)
    if url.scheme != "http":
        print("Only HTTP is supported")
        exit(1)

    request_headers = [
        f"GET {path} HTTP/1.1",
        f"Host: {host}",
        "Accept: */*",
        "Connection: close"
    ]
    request = "\r\n".join(request_headers) + "\r\n\r\n"

    if args.verbose:
        print("> " + "\n> ".join(request_headers) + "\n>")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode('utf-8'))
        response = b""
        while True:
            chunk = s.recv(2048)
            if not chunk:
                break
            response += chunk
        response_headers, response_data = response.decode('utf-8').split("\r\n\r\n", 1)
        if args.verbose:
            response_header_section = response_headers.split("\r\n")
            print("< " + "\n< ".join(response_header_section) + "\n<")
        print(response_data) 