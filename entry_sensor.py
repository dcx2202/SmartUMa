import datetime as Date
from threading import Timer
import raspbpi
import client

# Global variables
curr_date = Date.datetime.now()


# [Prob. Entering 00:00 -> 01:00, 01:00 -> 02:00, ...]
probs = [0, 0, 0, 0, 0, 0.05, 0.15, 1.25,
         2, 1.25, 0.3, 0.3, 0.25, 1.5, 1, 0.4,
         0.25, 0.15, 0.1, 0.1, 0.05, 0.05, 0, 0]


def main():
    global curr_date

    curr_date = Date.datetime.now()

    client.send_message_to_server("entry sensor connected.")

    if curr_date.second <= 56:  # If the a new minute is about to start, wait for the next one
        aux = 60
    else:
        aux = 120

    # Call start() "aux" seconds from now
    set_timeout(aux - 1 - curr_date.second + 0.0, start)


# Schedules a function call "timeout" seconds from now
def set_timeout(timeout, func):
    t = Timer(timeout, func)
    t.start()


def start():
    global curr_date

    while curr_date.second != 0:  # Waits for a new minute to start
        curr_date = Date.datetime.now()

    simulate()


def simulate():
    import random

    global curr_date

    curr_date = Date.datetime.now()  # Update the current date
    num_cars = raspbpi.get_num_cars()   # Get the current number of cars in the lot
    num_spaces = raspbpi.get_num_spaces()   # Get the total number of spaces

    # A car has entered
    if random.uniform(0, 100) < probs[curr_date.hour] and num_cars < num_spaces:
        # Send entry signal to server ("1" - 1 car entered)
        client.send_message_to_server("1")
        print("{} - a car entered".format(curr_date))

    set_timeout(1, simulate)    # Simulate again 1 second from now


if __name__ == "__main__":
    main()
