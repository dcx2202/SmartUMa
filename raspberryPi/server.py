import socket
import raspbpi
from datetime import datetime
from threading import Thread

# initialize server socket
server_address = ('localhost', 6789)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(server_address)
print('{} - starting the server'.format(datetime.now()))
print('Waiting for sensors to connect...')


# receives messages from client and prints
def communication_thread_function():
    while True:
        data, client = server.recvfrom(4096)

        if data.decode() == 'close':
            print('{} - closing the server'.format(datetime.now()))
            server.shutdown(socket.SHUT_RDWR)
            server.close()
            break
        elif data.decode() == 'print data':
            raspbpi.print_data()
        elif data.decode() == "request_cars":
            server.sendto(str.encode(str(raspbpi.get_num_cars())), client)
        else:
            process_socket_message(data, client)


# processes the messages received and updates data variables
def process_socket_message(data, client):
    curr_date = datetime.now()

    try:  # If it received an entry/exit signal
        # data hold the number of cars that entered/exited (positive/negative)
        data = int(data)

        # If cars entered then update the number of entries
        if data == 1 and raspbpi.get_num_cars() < raspbpi.get_num_spaces():
            raspbpi.new_entry(data)
            print("{} - a car entered".format(curr_date))
        elif data == -1 and raspbpi.get_num_cars() > 0:  # If cars exited then update the number of exits
            raspbpi.new_exit(-1 * data)
            print("{} - a car exited".format(curr_date))
        elif data == 2 and raspbpi.get_num_cars() > 0:
            raspbi.new_exit(data/2)
            print("{} - a car entered P1".format(curr_date))
        elif data == -2:
            print("{} - a car exited P1".format(curr_date))

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
