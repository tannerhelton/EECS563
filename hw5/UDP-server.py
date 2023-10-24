import socket
import os
import sys
import struct

def start_udp_server(port, save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('0.0.0.0', port))
        print(f"Server listening on port {port}")
        file_size_data, addr = s.recvfrom(4)
        file_size = struct.unpack('!I', file_size_data)[0]
        file_name_data, _ = s.recvfrom(20)
        file_name = file_name_data.decode().strip()
        with open(os.path.join(save_directory, file_name), 'wb') as f:
            remaining_bytes = file_size
            while remaining_bytes:
                data, _ = s.recvfrom(min(remaining_bytes, 4096))
                if not data:
                    break
                f.write(data)
                remaining_bytes -= len(data)

        print(f"File {file_name} saved successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 UDP-server.py <local-port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_udp_server(port, "received_files")