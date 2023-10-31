# Import necessary modules
import socket
import os
import sys
import struct

# Define the function to start a UDP server that listens for incoming files
def start_udp_server(port, save_directory):
    # Check if the save directory exists, if not, create it
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Bind the socket to all available interfaces and the specified port
        s.bind(('0.0.0.0', port))
        print(f"Server listening on port {port}")
        
        # Receive the size of the incoming file
        file_size_data, addr = s.recvfrom(4)
        file_size = struct.unpack('!I', file_size_data)[0]
        
        # Receive the file name
        file_name_data, _ = s.recvfrom(20)
        file_name = file_name_data.decode().strip()
        
        # Open the file in binary write mode to save the incoming data
        with open(os.path.join(save_directory, file_name), 'wb') as f:
            remaining_bytes = file_size
            while remaining_bytes:
                # Receive data from the client in chunks up to 4096 bytes
                data, _ = s.recvfrom(min(remaining_bytes, 4096))
                
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
        print("Usage: python3 UDP-server.py <local-port>")
        sys.exit(1)

    # Convert the provided port from string to integer
    port = int(sys.argv[1])
    
    # Call the start_udp_server function and set "received_files" as the default save directory
    start_udp_server(port, "received_files")
