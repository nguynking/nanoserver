from urllib.parse import urlparse
import sys

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

    print(f"connecting to {host}")
    print(f"Sending request GET {path} HTTP/1.1")
    print(f"Host: {host}")
    print(f"Accept: */*")