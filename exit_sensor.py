import datetime as Date
from threading import Timer
import client

# Global variables
curr_date = Date.datetime.now()


# [Prob. Exiting 00:00 -> 01:00, 01:00 -> 02:00, ...]
probs = [0.1, 0.1, 0, 0, 0, 0, 0.1, 0.1,
         0.1, 0.1, 0.1, 0.1, 1.2, 0.5, 0.8, 1,
         1, 1, 0.5, 0.5, 2.5, 2.5, 3, 9]


def main():
    global curr_date

    curr_date = Date.datetime.now()

    client.send_message_to_server("exit sensor connected")

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

    # Get a random number of cars that can leave
    #remove = random.randint(0, 5)
    remove = 1

    # A number (remove) of cars have left
    if random.uniform(0, 100) < probs[curr_date.hour]:
        for _ in range(remove):
            # Send exit signal to server (i.e. "-3" - 3 cars left)
            client.send_message_to_server(str(-1))
            print("{} - exit sensor sent a signal".format(curr_date))

    set_timeout(1, simulate)  # Simulate again 1 second from now


if __name__ == "__main__":
    main()
