# Import necessary modules
import socket
import os
import sys
import struct

# Define the function to start a TCP server that listens for incoming files
def start_tcp_server(port, save_directory):
    # Check if the save directory exists, if not, create it
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to all available interfaces and the specified port
        s.bind(('0.0.0.0', port))
        
        # Listen for incoming connections, with a backlog of 1
        s.listen(1)
        print(f"Server listening on port {port}")

        # Accept a connection from a client
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            
            # Receive the size of the incoming file
            file_size = struct.unpack('!I', conn.recv(4))[0]
            
            # Receive the file name
            file_name = conn.recv(20).decode().strip()
            
            # Open the file in binary write mode to save the incoming data
            with open(os.path.join(save_directory, file_name), 'wb') as f:
                remaining_bytes = file_size
                while remaining_bytes:
                    # Receive data from the client in chunks up to 4096 bytes
                    data = conn.recv(min(remaining_bytes, 4096))
                    
                    # If there's no data received, break from the loop
                    if not data:
                        break
                    
                    # Write the received data to the file
                    f.write(data)
                    remaining_bytes -= len(data)

    # Notify the user that the file has been saved successfully
    print(f"File {file_name} saved successfully.")

# This block is executed when the script is run as the main module
if __name__ == "__main__":
    # Ensure the correct number of command-line arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python3 TCP-server.py <local-port>")
        sys.exit(1)

    # Convert the provided port from string to integer
    port = int(sys.argv[1])
    
    # Call the start_tcp_server function and set "received_files" as the default save directory
    start_tcp_server(port, "received_files")
