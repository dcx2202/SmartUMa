from threading import Timer
import datetime as Date
import client

# Global variables
curr_date = Date.datetime.now()


# [Prob. Entering 00:00 -> 01:00, 01:00 -> 02:00, ...]
# Probabilidade de entrar no parque coberto é 1/10 das outras 
probs = [0, 0, 0, 0, 0, 0, 0.01, 0.04,
         0.25, 0.1, 0.03, 0.03, 0.02, 0.17, 0.07, 0.04,
         0.03, 0.02, 0.01, 0.01, 0.01, 0, 0, 0]


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
    curr_date = Date.datetime.now()  # Update the current date

    # A car has entered
    if random.uniform(0, 100) < probs[curr_date.hour]:
        # Send entry signal to server ("2" - 1 car entered the interior park)
        # Entrada no parque coberto = saida do parque exterior
        client.send_message_to_server("2")
        print("{} - entry sensor sent a signal".format(curr_date))

    set_timeout(1, simulate)    # Simulate again 1 second from now


if __name__ == "__main__":
    main()
