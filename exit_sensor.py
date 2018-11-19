import datetime as Date
from threading import Timer
import raspbpi

# Global variables
curr_date = Date.datetime.now()


# [Prob. Exiting 00:00 -> 01:00, 01:00 -> 02:00, ...]
probs = [0.05, 0.05, 0, 0, 0, 0, 0.05, 0.05,
         0.05, 0.05, 0.05, 0.05, 0.6, 0.25, 0.4,
         0.5, 0.5, 0.5, 0.25, 0.25, 1.25, 1.25, 1.5, 4.5]


def main():
    global curr_date

    curr_date = Date.datetime.now()

    if curr_date.second <= 56:  # If the a new minute is about to start, wait for the next one
        aux = 60
    else:
        aux = 120

    set_timeout(aux - 1 - curr_date.second + 0.0, start) # Call start() "aux" seconds from now


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
    import client

    global curr_date

    curr_date = Date.datetime.now()  # Update the current date
    num_cars = raspbpi.get_num_cars()   # Get the current number of cars in the lot

    remove = random.randint(0, 5)   # Get a random number of cars that can leave

    if random.uniform(0, 100) < probs[curr_date.hour] and num_cars >= remove > 0:   # A number (remove) of cars have left
        client.send_message_to_server(str(-remove))    # Send exit signal to server (i.e. "-3" - 3 cars left)
        print("Saiu ", remove, " carro(s) as ", curr_date.hour, "h", curr_date.minute, "m")

    set_timeout(1, simulate) # Simulate again 1 second from now


if __name__ == "__main__":
    main()