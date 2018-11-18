import datetime as Date

num_cars = 0    # TODO - Fazer alguma coisa com isto - Estas variaveis e estatisticas deviam ficar num modulo separado
num_spaces = 0
num_entries = 0
num_exits = 0
spaces = [] # TODO - Quanto tempo guardamos o historico? Se calhar e mais facil com uma pequena db do que tornar o array muito complexo e arriscar perder tudo se o programa crashar
for i in range(24):
    spaces.append(0)


def get_num_cars():
    return num_cars


def set_num_cars(num):
    global num_cars
    num_cars = num


def update_num_cars(num):
    global num_cars
    num_cars += num


def get_num_spaces():
    return num_spaces


def get_num_entries():
    return num_entries


def update_num_entries(num):
    global num_entries
    num_entries += num


def get_num_exits():
    return num_exits


def update_num_exits(num):
    global num_exits
    num_exits += num


def update_num_spaces():
    spaces[Date.datetime.now().hour] = num_cars


def new_entry(data):
    update_num_entries(data)
    update_num_cars(data)  # Update the number of cars
    update_num_spaces() # Update the number of spaces

    # Do something (update stats, store info, ...)


def new_exit(data):
    update_num_exits(data)
    update_num_cars(-data)  # Update the number of cars
    update_num_spaces()  # Update the number of spaces

    # Do something (update stats, store info, ...)
