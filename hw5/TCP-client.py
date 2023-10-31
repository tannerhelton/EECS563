# Import necessary modules
import socket
import os
import sys
import struct

# Define the function to send a file to a server
def send_file_to_server(server_ip, server_port, file_path):
    # Check if the specified file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Get the size and name of the file
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server using provided IP and port
        s.connect((server_ip, server_port))
        
        # Send the file size first
        s.sendall(struct.pack('!I', file_size))
        
        # Send the file name 
        s.sendall(f"{file_name: <20}".encode())
        
        # Open the file in binary mode and send its content
        with open(file_path, 'rb') as f:
            while True:
                # Read 4096 bytes at a time from the file
                data = f.read(4096)
                
                # If there's no more data to read, break from the loop
                if not data:
                    break
                
                # Send the read data to the server
                s.sendall(data)

    # Notify the user that the file has been sent successfully
    print(f"File {file_name} sent successfully.")

# This block is executed when the script is run as the main module
if __name__ == "__main__":
    # Ensure the correct number of command-line arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python3 TCP-client.py <remote-IP> <remote-port> <local-file-path>")
        sys.exit(1)

    # Extract the command-line arguments
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])  # Convert the port from string to integer
    file_path = sys.argv[3]
    
    # Call the send_file_to_server function
    send_file_to_server(server_ip, server_port, file_path)
