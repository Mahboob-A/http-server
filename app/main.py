# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    print('server started...')

    OK_200 = b'HTTP/1.1 200 OK\r\n'
    NOT_FOUND_404 = b'HTTP/1.1 404 Not Found\r\n'
    END_HEADER = b'\r\n'
    CONTENT_TYPE = b'Content-Type: text/plain\r\n'

    def get_content_length(content): 
        return f"Content-Length: {len(content)}\r\n".encode('utf-8')

    tmp = None 
    while True: 
        try: 
            conn, addr = server_socket.accept() 
            with conn: 
                print('Server connected to {}:{}'.format(addr[0], addr[1]))

                # all data in bytes
                data = conn.recv(1024)
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
        except: 
            print('Server closed!')
            server_socket.close()
            break


if __name__ == "__main__":
    main()
