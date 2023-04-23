import socket
from urllib.parse import urlparse
import time

# Define the Matrix screen size
ROWS = 30
COLS = 80

# Define the color codes for the Matrix interface
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

# Define a function to print a Matrix character at a given position
def print_matrix_char(row, col, char, color=GREEN):
    print(f"\033[{row};{col}H{color}{char}{ENDC}", end='', flush=True)

# Set the target URL and range of ports to scan
target_url = input("Enter the target URL: ")
start_port = int(input("Enter the start port: "))
end_port = int(input("Enter the end port: "))

# Parse the target URL to get the hostname and scheme
parsed_url = urlparse(target_url)
target_host = parsed_url.hostname
if parsed_url.scheme == 'https':
    start_port = 443
    end_port = 443
elif parsed_url.scheme == 'http':
    start_port = 80
    end_port = 80

# Initialize the Matrix interface with random characters
for row in range(ROWS):
    for col in range(COLS):
        print_matrix_char(row, col, chr(65 + row % 26))

# Iterate over the range of ports to scan
for port in range(start_port, end_port+1):
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set the socket timeout to 1 second
    sock.settimeout(1)
    try:
        # Attempt to connect to the target host on the current port
        result = sock.connect_ex((target_host, port))
        # If the connection was successful, print the open port number in red
        if result == 0:
            row = int(time.time() * 1000) % ROWS
            col = int(port / end_port * COLS)
            print_matrix_char(row, col, str(port), color=RED)
    except:
        pass
    finally:
        # Close the socket connection
        sock.close()
