# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True: 
        try: 
            conn, addr = server_socket.accept() 
            with conn: 
                print('Server connected to {}:{}'.format(addr[0], addr[1]))
                data = conn.recv(1024).encode('utf-8')
                conn.send('HTTP/1.1 OK\r\n\r\n'.encode('utf-8'))
        except: 
            print('Server closed!')
            server_socket.close()
            break
    


if __name__ == "__main__":
    main()
