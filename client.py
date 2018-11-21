import socket
from datetime import datetime

# initialize client socket
server_address = ('localhost', 6789)
print('{} - starting the client'.format(datetime.now()))
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# sends a message to server
def send_message_to_server(message):
    client.sendto(str.encode(message), server_address)


# receives a message from server
def receive_message():
    response, server = client.recvfrom(4096)
    return response.decode()


# closes the sockets
def close_sockets():
    print('{} - closing the client'.format(datetime.now()))
    client.sendto(str.encode('close'), server_address)
    client.shutdown(socket.SHUT_RDWR)
    client.close()
