import socket

from datetime import datetime

# initialize client socket
server_address = ('10.2.211.51', 6789)
print('Starting the client at', datetime.now())
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# sends a message to server
def send_message_to_server(message):
    client.sendto(str.encode(message), server_address)


# closes the sockets
def close_sockets():
    print('Closing the server at', datetime.now())
    client.sendto(str.encode('close'), server_address)
    client.shutdown(socket.SHUT_RDWR)
    client.close()
