from urllib.parse import urlparse
import socket
import argparse

def validate_url(new_path, original_url=None):
    if original_url is None:
        original_url = ""
    if new_path.startswith("//"):
        new_path = "http:" + new_path
    elif new_path.startswith("/"):
        url = urlparse(original_url)
        scheme = url.scheme
        hostname = url.hostname
        if not scheme or not hostname:
            print("Invalid original URL for relative path")
            exit(1)
        new_path = f"{scheme}://{hostname}{new_path}"
    parsed_url = urlparse(new_path)
    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 80
    path = parsed_url.path if parsed_url.path else "/"

    if host is None:
        print("Invalid URL")
        exit(1)
    if parsed_url.scheme != "http":
        print("Only HTTP is supported")
        exit(1)
    return host, port, path

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
        return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Curl-like tool")
    parser.add_argument("url", type=str, help="URL to fetch")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-X", "--method", type=str, default="GET", help="HTTP method to use")
    parser.add_argument("-d", "--data", type=str, help="Data to send in the request body")
    parser.add_argument("-H", "--header", action="append", type=str, help="Additional headers to send")
    parser.add_argument("-L", "--location", action="store_true", help="Follow redirects")
    args = parser.parse_args()

    host, port, path = validate_url(args.url)
    if args.method not in ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]:
        print("Invalid HTTP method")
        exit(1)

    response = send_request(
        host,
        port,
        path,
        args.method,
        args.data,
        args.header,
        args.verbose
    )

    if args.location:
        count_redirects = 3
        while count_redirects > 0:
            response_headers, response_data = response.decode("utf-8").split("\r\n\r\n", 1)
            response_headers_lines = response_headers.split("\r\n")
            for header in response_headers_lines:
                if header.startswith("HTTP"):
                    status_code = header.split(" ")[1]
                    if not status_code.startswith("3"):
                        exit(1)
                if header.startswith("Location:"):
                    host, port, path = validate_url(header.split(" ")[1], args.url)
                    break
            
            response = send_request(
                host,
                port,
                path,
                args.method,
                args.data,
                args.header,
                args.verbose
            )
            count_redirects -= 1
            if count_redirects == 0:
                print("Max redirects reached")
                exit(1)