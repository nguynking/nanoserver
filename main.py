import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 8080))
s.listen()

while True:
    conn, addr = s.accept()
    print(f"Connected by {addr}")

    data = conn.recv(1024)
    print(data.decode('utf-8'))

    request_line = data.decode('utf-8').split("\r\n")[0]
    method, path, protocol = request_line.split(' ')

    if path == "/" or path == "/index.html":
        with open('index.html', 'rb') as f:
            file = f.read()
        response = f"HTTP/1.1 200 OK\r\n\r\n{file.decode('utf-8')}\r\n"
    else:
        response = "HTTP/1.1 404 Not Found\r\n"
    conn.sendall(response.encode('utf-8'))
    conn.close()