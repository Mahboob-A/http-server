# Uncomment this to pass the first stage
import socket
import threading
import sys
from concurrent.futures import ThreadPoolExecutor

OK_200 = "HTTP/1.1 200 OK\r\n"
NOT_FOUND_404 = "HTTP/1.1 404 Not Found\r\n"
END_HEADER = "\r\n"
BODY_END_HEADER = "\r\n"
CONTENT_TYPE = "Content-Type: text/plain\r\n"


def get_content_length(content):
    return f"Content-Length: {len(content)}\r\n"


def handle_connections(conn):
    data = conn.recv(1024).decode('utf-8')
    headers = data.split()
    path = headers[1]

    print("headers: ", headers)
    print("path: ", path)


    if path == "/":
        response = OK_200 + END_HEADER
        conn.send(response.encode("utf-8"))
    elif "/echo/" in path: 
        body_data = path[6:]  
        print(body_data)
        CONTENT_LENGTH = get_content_length(body_data)
        response = (
            OK_200 + CONTENT_TYPE + CONTENT_LENGTH + END_HEADER + body_data + BODY_END_HEADER
        )
        conn.send(response.encode('utf-8'))
    elif "/user-agent" in path:
        user_agent = headers[6]  # user_agent:  b'curl/7.81.0'
        print("user_agent: ", user_agent)
        CONTENT_LENGTH = get_content_length(user_agent)
        response = (
            OK_200 + CONTENT_TYPE + CONTENT_LENGTH + END_HEADER + user_agent + BODY_END_HEADER
        )
        conn.send(response.encode("utf-8"))
    else:
        response = NOT_FOUND_404 + END_HEADER
        conn.send(response.encode("utf-8"))


def main():
    print("Server is starting ... ")
    HOST = "127.0.0.1"
    PORT = 4221

    # try:
    socket_server = socket.create_server((HOST, PORT), reuse_port=False)
    while True:
        conn, addr = socket_server.accept()
        print("Connected to: {}:{}".format(addr[0], addr[1]))
        worker = threading.Thread(target=handle_connections, args=(conn,))
        worker.start()
    # except KeyboardInterrupt:
    #     print("Server is shutting down...")
    #     sys.exit(0)
    # except Exception as e:
    #     print("An error occurred:", e)
    #     sys.exit(1)


if __name__ == "__main__":
    main()
