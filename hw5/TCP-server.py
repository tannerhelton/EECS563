import socket
import os
import sys
import struct

def start_tcp_server(port, save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f"Server listening on port {port}")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            file_size = struct.unpack('!I', conn.recv(4))[0]
            file_name = conn.recv(20).decode().strip()
            with open(os.path.join(save_directory, file_name), 'wb') as f:
                remaining_bytes = file_size
                while remaining_bytes:
                    data = conn.recv(min(remaining_bytes, 4096))
                    if not data:
                        break
                    f.write(data)
                    remaining_bytes -= len(data)

    print(f"File {file_name} saved successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 TCP-server.py <local-port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_tcp_server(port, "received_files")