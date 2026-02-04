from urllib.parse import urlparse
import socket
import argparse

def send_request(host, port, path, method, data, headers, verbose):
    request_headers = [
        f"{method} {path} HTTP/1.1",
        f"Host: {host}",
        "Accept: */*",
        "Connection: close"
    ]
    if headers:
        request_headers.extend(headers)
    if data:
        request_headers.append(f"Content-Length: {len(data.encode('utf-8'))}")

    request = "\r\n".join(request_headers) + "\r\n\r\n"

    if data:
        request += data

    if verbose:
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
        if verbose:
            response_header_section = response_headers.split("\r\n")
            print("< " + "\n< ".join(response_header_section) + "\n<")
        print(response_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Curl-like tool")
    parser.add_argument("url", type=str, help="URL to fetch")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-X", "--method", type=str, default="GET", help="HTTP method to use")
    parser.add_argument("-d", "--data", type=str, help="Data to send in the request body")
    parser.add_argument("-H", "--header", action="append", type=str, help="Additional headers to send")
    args = parser.parse_args()

    url = urlparse(args.url)
    host = url.hostname
    port = url.port if url.port else 80
    path = url.path if url.path else "/"

    if host is None:
        print("Invalid URL")
        exit(1)
    if args.method not in ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]:
        print("Invalid HTTP method")
        exit(1)
    if url.scheme != "http":
        print("Only HTTP is supported")
        exit(1)

    send_request(
        host,
        port,
        path,
        args.method,
        args.data,
        args.header,
        args.verbose
    )