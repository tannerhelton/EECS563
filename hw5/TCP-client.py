import socket
import os
import struct

def send_file_to_server(server_ip, server_port, file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        s.sendall(struct.pack('!I', file_size))
        s.sendall(f"{file_name: <20}".encode())
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                s.sendall(data)

    print(f"File {file_name} sent successfully.")

send_file_to_server("127.0.0.1", 12345, "test.txt")