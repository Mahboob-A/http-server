# Uncomment this to pass the first stage
import socket
import threading
import sys
import os
import argparse
import mimetypes

OK_200 = "HTTP/1.1 200 OK\r\n"
NOT_FOUND_404 = "HTTP/1.1 404 Not Found\r\n"
END_HEADER = "\r\n"
BODY_END_HEADER = "\r\n"
CONTENT_TYPE = "Content-Type: text/plain\r\n"
FILE_CONTENT_TYPE = "Content-Type: application/octet-stream"


def get_content_length(content):
    return f"Content-Length: {len(content)}\r\n"


def handle_connections(conn, directory):
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
    elif ("/files/" in path):  
        print('dir: ', directory)
        file_path = os.path.join(directory, path[7:])
        print('curr-dir: ', os.getcwd())
        print('file path: ', file_path)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file_contents = f.read()
                print('file-contents: ', file_contents)
            conn.send(
                f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file_contents)}\r\n\r\n".encode()
                + file_contents 
            )
        else:
            response = NOT_FOUND_404 + END_HEADER
            conn.send(response.encode("utf-8"))
    else:
        response = NOT_FOUND_404 + END_HEADER
        conn.send(response.encode("utf-8"))
        
    conn.close()


def main():
    print("Server is starting ... ")
    HOST = "127.0.0.1"
    PORT = 4221
    curr_dir = os.getcwd()
    # try:
    socket_server = socket.create_server((HOST, PORT), reuse_port=False)
    while True:
        conn, addr = socket_server.accept()
        print("Connected to: {}:{}".format(addr[0], addr[1]))
        worker = threading.Thread(target=handle_connections, args=(conn, curr_dir))
        worker.start()
    # except KeyboardInterrupt:
    #     print("Server is shutting down...")
    #     sys.exit(0)
    # except Exception as e:
    #     print("An error occurred:", e)
    #     sys.exit(1)


if __name__ == "__main__":
    main()
