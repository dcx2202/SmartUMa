import datetime as Date
from threading import Timer
import client

# Global variables
curr_date = Date.datetime.now()


# [Prob. Exiting 00:00 -> 01:00, 01:00 -> 02:00, ...]
probs = [0.05, 0.05, 0, 0, 0, 0, 0.05, 0.05,
         0.05, 0.05, 0.05, 0.05, 0.6, 0.25, 0.4,
         0.5, 0.5, 0.5, 0.25, 0.25, 1.25, 1.25, 1.5, 4.5]


def main():
    client.send_message_to_server("exit sensor connected")
    simulate()


# Schedules a function call "timeout" seconds from now
def set_timeout(timeout, func):
    t = Timer(timeout, func)
    t.start()


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
