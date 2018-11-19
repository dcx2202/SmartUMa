import socket
from datetime import datetime
from threading import Thread
import raspbpi

# initialize server socket
server_address = ('10.2.211.51', 6789)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(server_address)
print(datetime.now(), '- starting the server')
print('Waiting for sensors to connect...')


# receives messages from client and prints
def communication_thread_function():
    printed = False
    while True:
        max_size = 4096
        data, client = server.recvfrom(max_size)

        if not printed and datetime.now().minute == 0:
            raspbpi.print_data()
            printed = True

        if datetime.now().minute != 0:
            printed = False

        if data.decode() == 'close':
            print(datetime.now(), '- closing the server at')
            server.shutdown(socket.SHUT_RDWR)
            server.close()
            break

        process_socket_message(data, client)


# processes the messages received and updates data variables
def process_socket_message(data, client):

    curr_date = datetime.now()

    try:  # If it received an entry/exit signal
        # data hold the number of cars that entered/exited (positive/negative)
        data = int(data)

        # If cars entered then update the number of entries
        if data > 0 and raspbpi.get_num_cars() < raspbpi.get_num_spaces():
            raspbpi.new_entry(data)
            print("{} - a car entered".format(curr_date))
        elif data < 0 and raspbpi.get_num_cars() > 0:  # If cars exited then update the number of exits
            raspbpi.new_exit(-1 * data)
            print("{} - a car exited".format(curr_date))

    except:     # Received a text message (sensor connected, ...)
        # Do something with this
        print(str(curr_date) + ' - ' + str(data.decode()))


def initialize_communication_thread():
    communication_thread = Thread(
        target=communication_thread_function, args=())
    communication_thread.start()
    communication_thread.join()


def main():
    initialize_communication_thread()


if __name__ == '__main__':
    main()