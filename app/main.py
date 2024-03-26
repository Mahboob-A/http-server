# Uncomment this to pass the first stage
import socket
import threading
import sys 


OK_200 = b'HTTP/1.1 200 OK\r\n'
NOT_FOUND_404 = b'HTTP/1.1 404 Not Found\r\n'
END_HEADER = b'\r\n'
CONTENT_TYPE = b'Content-Type: text/plain\r\n'

def get_content_length(content): 
    return f"Content-Length: {len(content)}\r\n".encode('utf-8')

def handle_connections(conn): 
    with conn: 
        # all data in bytes
        data = conn.recv(1024)
        if data: 
            headers = data.split(b'\r\n')
            path = headers[0].split()[1]
            user_agent = headers[2].split()[1]  # user_agent:  b'curl/7.81.0'

            print('headers: ', headers)
            print('path: ', path)
            print('user_agent: ', user_agent)

            if path == b'/': 
                response = OK_200 + END_HEADER
            elif path.startswith(b'/echo/'):
                body_data = path[6:] # already in bytes 
                CONTENT_LENGTH = get_content_length(body_data)
                response = OK_200 +  CONTENT_TYPE + CONTENT_LENGTH + END_HEADER + body_data
            elif path == b'/user-agent': 
                CONTENT_LENGTH = get_content_length(user_agent)
                response = OK_200 + CONTENT_TYPE + CONTENT_LENGTH + END_HEADER + user_agent
            else: 
                response = NOT_FOUND_404 + END_HEADER 
            # response
            conn.send(response)
        else: 
            response = NOT_FOUND_404 + END_HEADER
            # response
            conn.send(response)    


def main():
    print("Server is starting ... ")
    HOST = "127.0.0.1"
    PORT = 4221

    try:
        socket_server = socket.create_server((HOST, PORT), reuse_port=False)
        while True:
            conn, addr = socket_server.accept()
            print("Connected to: {}:{}".format(addr[0], addr[1]))
            worker = threading.Thread(target=handle_connections, args=(conn,))
            worker.start()
    except KeyboardInterrupt:
        print("Server is shutting down...")
        sys.exit(0)
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
