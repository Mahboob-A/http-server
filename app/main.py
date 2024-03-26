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
                # print(data)
                data = data.split('\r\n')
                # print(data)
                data = data[2].split(' ')
                # print(data)
                header = data[1]
                # print(header)

                CONTENT_TYPE = 'Content-Type: text/plain\r\n'
                CONTENT_LENGTH = f'Content-Length: {len(header)}\r\n'
                response = (OK_200 +  CONTENT_TYPE + CONTENT_LENGTH + END_HEADER + header).encode('utf-8')
                conn.send(response)
        except: 
            print('Server closed!')
            server_socket.close()
            break


if __name__ == "__main__":
    main()
