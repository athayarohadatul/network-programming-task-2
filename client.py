from socket import socket, AF_INET, SOCK_STREAM

def main():
    server_address = ('localhost', 45000)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(server_address)

    try:
        while True:
            message = input("Enter command (TIME or QUIT): ").strip().upper()
            if message in ("TIME", "QUIT"):
                client_socket.sendall(f"{message}\r\n".encode('utf-8'))
                if message == "TIME":
                    response = client_socket.recv(1024)
                    print("Received:", response.decode('utf-8').strip())
                else:
                    print("Connection closed.")
                    break
            else:
                print("Invalid command. Please enter TIME or QUIT.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
