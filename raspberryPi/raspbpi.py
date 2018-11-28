import datetime as Date
import db_manager

num_cars = 0
num_spaces = 130
num_entries = 0
num_exits = 0
spaces = []

for i in range(24):
    spaces.append(0)


def get_num_cars():
    return int(num_cars)


def update_num_cars(num):
    global num_cars
    num_cars += num


def get_num_spaces():
    return int(num_spaces)


def get_num_entries():
    return int(num_entries)


def update_num_entries(num):
    global num_entries
    num_entries += num


def get_num_exits():
    return int(num_exits)


def update_num_exits(num):
    global num_exits
    num_exits += num


def get_spaces():
    global spaces
    return spaces


def update_num_spaces():
    spaces[Date.datetime.now().hour] = num_cars


def new_entry(data):
    update_num_entries(data)
    update_num_cars(data)  # Update the number of cars
    update_num_spaces()    # Update the number of spaces
    db_manager.insert_entry_to_db(
        Date.datetime.now().date(), Date.datetime.now().time(), get_num_cars())

    # Do something (update stats, store info, ...)


def new_exit(data):
    update_num_exits(data)
    update_num_cars(-data)  # Update the number of cars
    update_num_spaces()  # Update the number of spaces
    db_manager.insert_exit_to_db(
        Date.datetime.now().date(), Date.datetime.now().time(), get_num_cars())

    # Display something
    # Do something (update stats, store info, ...)


def print_data():
    print("Num cars:", get_num_cars())
    print("Num entries:", get_num_entries())
    print("Num exits:", get_num_exits())
    print("Num spaces:", get_spaces())
