import socket

from datetime import datetime

# initialize client socket
server_address = ('10.2.211.51', 6789)
print(datetime.now(), '- starting the client')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# sends a message to server
def send_message_to_server(message):
    client.sendto(str.encode(message), server_address)


# closes the sockets
def close_sockets():
    print(datetime.now(), '- closing the server')
    client.sendto(str.encode('close'), server_address)
    client.shutdown(socket.SHUT_RDWR)
    client.close()
