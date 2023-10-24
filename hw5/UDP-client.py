import socket
import os
import sys
import struct

def send_file_to_udp_server(server_ip, server_port, file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(struct.pack('!I', file_size), (server_ip, server_port))
        s.sendto(f"{file_name: <20}".encode(), (server_ip, server_port))
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                s.sendto(data, (server_ip, server_port))

    print(f"File {file_name} sent successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 UDP-client.py <remote-IP> <remote-port> <local-file-path>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    file_path = sys.argv[3]
    send_file_to_udp_server(server_ip, server_port, file_path)