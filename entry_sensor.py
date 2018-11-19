import datetime as Date
from threading import Timer
import client

# Global variables
curr_date = Date.datetime.now()


# [Prob. Entering 00:00 -> 01:00, 01:00 -> 02:00, ...]
probs = [0, 0, 0, 0, 0, 0.05, 0.15, 1.25,
         2, 1.25, 0.3, 0.3, 0.25, 1.5, 1, 0.4,
         0.25, 0.15, 0.1, 0.1, 0.05, 0.05, 0, 0]


def main():
    client.send_message_to_server("entry sensor connected")
    simulate()


# Schedules a function call "timeout" seconds from now
def set_timeout(timeout, func):
    t = Timer(timeout, func)
    t.start()


def simulate():
    import random

    global curr_date
    print("simulating ", curr_date)
    curr_date = Date.datetime.now()  # Update the current date

    # A car has entered
    if random.uniform(0, 100) < probs[curr_date.hour]:
        # Send entry signal to server ("1" - 1 car entered)
        client.send_message_to_server("1")
        print("{} - entry sensor sent a signal".format(curr_date))

    set_timeout(1, simulate)    # Simulate again 1 second from now


if __name__ == "__main__":
    main()
