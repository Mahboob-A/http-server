import socket
import threading


def handle_conn(conn):
    data = conn.recv(2048).decode()
    lines = data.split("\r\n")
    first_line = lines[0]
    path = first_line.split()[1]
    if path == "/":
        conn.send("HTTP/1.1 200 OK\r\n\r\n".encode())
    elif path[:6] == "/echo/":
        string = path[6:]
        conn.send("HTTP/1.1 200 OK\r\n".encode())
        conn.send("Content-Type: text/plain\r\n".encode())
        conn.send(f"Content-Length: {len(string)}\r\n\r\n".encode())
        conn.send(f"{string}".encode())
    elif path == "/user-agent":
        user_agent = lines[2].split()[1]
        conn.send("HTTP/1.1 200 OK\r\n".encode())
        conn.send("Content-Type: text/plain\r\n".encode())
        conn.send(f"Content-Length: {len(user_agent)}\r\n\r\n".encode())
        conn.send(f"{user_agent}".encode())
    else:
        conn.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())


def main():
    print('server started...')
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, addr = server_socket.accept()  # wait for client
        threading.Thread(target=handle_conn, args=[conn]).start()


if __name__ == "__main__":
    main()
