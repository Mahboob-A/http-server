# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print('server started...')
    
    OK_200 = 'HTTP/1.1 200 OK\r\n'
    NOT_FOUND_404 = 'HTTP/1.1 404 Not Found\r\n'
    END_HEADER = '\r\n'
    
    while True: 
        try: 
            conn, addr = server_socket.accept() 
            with conn: 
                print('Server connected to {}:{}'.format(addr[0], addr[1]))
                data = conn.recv(1024).decode('utf-8')
                print(data)
                data = data.split('\r\n')
                print(data)
                data = data[0].split(' ')
                print(data)
                path = data[1]
                print(path)
                # data.split('\r\n')
                # ['GET /index.html HTTP/1.1', 'Host: localhost:4221', 'User-Agent: curl/7.81.0', 'Accept: */*', '', '']

                # data[0].split(' ')
                # GET /index.html HTTP/1.1

                # data[1] # /index.html
                # ['GET', '/index.html', 'HTTP/1.1']

                if path == '/': 
                    response = "HTTP/1.1 200 OK\r\n\r\n".encode("utf-8")
                elif path.startswith('/echo/'):
                    body_data = path[6:]
                    CONTENT_TYPE = 'Content-Type: text/plain\r\n'
                    CONTENT_LENGTH = f'Content-Length: {len(body_data)}\r\n'
                    response = (OK_200 +  CONTENT_TYPE + CONTENT_LENGTH + END_HEADER + body_data).encode('utf-8')
                else: 
                    response = "HTTP/1.1 404 Not Found\r\n\r\n".encode("utf-8")
                conn.send(response)
        except: 
            print('Server closed!')
            server_socket.close()
            break


if __name__ == "__main__":
    main()
