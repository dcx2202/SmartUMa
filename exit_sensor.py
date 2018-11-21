from threading import Timer
import datetime as Date
import client

# Global variables
curr_date = Date.datetime.now()


# [Prob. Exiting 00:00 -> 01:00, 01:00 -> 02:00, ...]
probs = [0.1, 0.1, 0, 0, 0, 0, 0.1, 0.1,
         0.1, 0.1, 0.1, 0.1, 1.2, 0.5, 0.8,
         1, 1, 1, 0.5, 0.5, 2.5, 1, 0.2, 0.1]


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

    # A car has left
    if random.uniform(0, 100) < probs[curr_date.hour]:
        # Send request for number of cars
        client.send_message_to_server("request_cars")
        # waits for response
        response = client.receive_message()

        if int(response) > 0:
            # Send exit signal to server
            client.send_message_to_server("-1")
            print("{} - exit sensor sent a signal".format(curr_date))

    set_timeout(1, simulate)  # Simulate again 1 second from now


if __name__ == "__main__":
    main()
