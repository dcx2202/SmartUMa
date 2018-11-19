import socket
from datetime import datetime
from threading import Thread
import raspbpi

# initialize server socket
server_address = ('10.2.211.51', 6789)
print('Starting the server at', datetime.now())
print('Waiting for sensors to connect...')
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(server_address)


# receives messages from client and prints
def communication_thread_function():
    while True:
        max_size = 4096
        data, client = server.recvfrom(max_size)

        if data.decode() == 'close':
            print('Closing the server at', datetime.now())
            server.shutdown(socket.SHUT_RDWR)
            server.close()
            break

        process_socket_message(data, client)


# processes the messages received and updates data variables
def process_socket_message(data, client):

    curr_date = datetime.now()

    try: # If it received an entry/exit signal
        data = int(data)    # data hold the number of cars that entered/exited (positive/negative)

        if data > 0:    # If cars entered then update the number of entries
            raspbpi.new_entry(data)
            print("Entrou um carro - {}".format(curr_date))
        elif data < 0:  # If cars exited then update the number of exits
            raspbpi.new_exit(-1 * data)
            print("Saiu um carro - {}".format(curr_date))


    except:     # Received a text message (sensor connected, ...)
        print(data.decode())     # Do something with this


def initialize_communication_thread():
    communication_thread = Thread(target=communication_thread_function, args=())
    communication_thread.start()
    communication_thread.join()


def main():
    initialize_communication_thread()


if __name__ == '__main__':
    main()
