import datetime as Date
from threading import Timer
import raspbpi

# Global variables
currDate = Date.datetime.now()


# [Prob. Entering 00:00 -> 01:00, 01:00 -> 02:00, ...]
probs = [0, 0, 0, 0, 0, 0.05, 0.15, 1.25,
         2, 1.25, 0.3, 0.3, 0.25, 1.5, 1, 0.4,
         0.25, 0.15, 0.1, 0.1, 0.05, 0.05, 0, 0]


def main():
    global currDate

    currDate = Date.datetime.now()

    if currDate.second <= 56:  # If the a new minute is about to start, wait for the next one
        aux = 60
    else:
        aux = 120

    set_timeout(aux - 1 - currDate.second + 0.0, start) # Call start() "aux" seconds from now


# Schedules a function call "timeout" seconds from now
def set_timeout(timeout, func):
    t = Timer(timeout, func)
    t.start()


def start():
    global currDate

    while currDate.second != 0:  # Waits for a new minute to start
        currDate = Date.datetime.now()

    simulate()


def simulate():
    import random
    import client

    global currDate

    currDate = Date.datetime.now()  # Update the current date
    num_cars = raspbpi.get_num_cars()   # Get the current number of cars in the lot
    num_spaces = raspbpi.get_num_spaces()   # Get the total number of spaces

    if random.uniform(0, 100) < probs[currDate.hour][0] and num_cars < num_spaces:  # A car has entered
        client.send_message_to_server("1")  # Send entry signal to server ("1" - 1 car entered)
        print("Entrou um carro as ", currDate.hour, "h", currDate.minute, "m")

    set_timeout(1, simulate)    # Simulate again 1 second from now


if __name__ == "__main__":
    main()
