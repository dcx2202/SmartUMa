import mysql.connector as mysql
from datetime import datetime

num_spaces = 130

# connect to database
mydb = mysql.connect(
    host='localhost',
    user='root',
    passwd='sdpass',
    database='smart_uma_parking_sensors_db'
)

mycursor = mydb.cursor()


# inserts a new entry to the respective table in the DB
def insert_entry_to_db(date, time, n_cars):
    sql = "INSERT INTO entry_sensor_tab (date, time, num_cars) VALUES (%s, %s, %s)"
    val = (date, time, n_cars)

    mycursor.execute(sql, val)
    mydb.commit()


# inserts a new exit to the respective table in the DB
def insert_exit_to_db(date, time, n_cars):
    sql = "INSERT INTO exit_sensor_tab (date, time, num_cars) VALUES (%s, %s, %s)"
    val = (date, time, n_cars)

    mycursor.execute(sql, val)
    mydb.commit()


# gets the number of parked cars at this moment from the DB
def get_num_cars_parked_from_db():
    sql = 'SELECT * FROM entry_sensor_tab ORDER BY id DESC LIMIT 1'
    mycursor.execute(sql)
    last_entry = mycursor.fetchall()[0]

    sql = 'SELECT * FROM exit_sensor_tab ORDER BY id DESC LIMIT 1'
    mycursor.execute(sql)
    last_exit = mycursor.fetchall()[0]

    n_cars = 0

    if last_entry[1] > last_exit[1]:
        n_cars = last_entry[3]
    elif last_entry[1] < last_exit[1]:
        n_cars = last_exit[3]
    elif last_entry[2] > last_exit[2]:
        n_cars = last_entry[3]
    else:
        n_cars = last_exit[3]

    return n_cars


# gets the number of entries in the previous hour from the DB
def get_num_entries_last_hour_from_db():
    sql = 'SELECT COUNT(*) FROM entry_sensor_tab WHERE CONCAT(date, \' \', time) >= DATE_SUB(NOW(), INTERVAL 1 HOUR)'
    mycursor.execute(sql)

    return mycursor.fetchall()[0][0]


# gets the number of exits in the previous hour from the DB
def get_num_exits_last_hour_from_db():
    sql = 'SELECT COUNT(*) FROM exit_sensor_tab WHERE CONCAT(date, \' \', time) >= DATE_SUB(NOW(), INTERVAL 1 HOUR)'
    mycursor.execute(sql)

    return mycursor.fetchall()[0][0]


# gets the number of free parking spaces from the DB
def get_num_free_spaces_from_db():
    return num_spaces - get_num_cars_parked_from_db()


# TODO
# gets data from the DB and calculates some statistics
def get_statistics():
    return 0


# gets log of the last day from the DB
def get_last_24h_log_from_database():
    sql = 'SELECT * FROM entry_sensor_tab WHERE CONCAT(date, \' \', time) >= DATE_SUB(NOW(), INTERVAL 24 HOUR)'
    mycursor.execute(sql)
    entry_log = mycursor.fetchall()

    row_headers = [x[0] for x in mycursor.description]
    json_data_1 = []
    for row in entry_log:
        json_data_1.append(dict(zip(row_headers, row)))

    sql = 'SELECT * FROM exit_sensor_tab WHERE CONCAT(date, \' \', time) >= DATE_SUB(NOW(), INTERVAL 24 HOUR)'
    mycursor.execute(sql)
    exit_log = mycursor.fetchall()

    row_headers = [x[0] for x in mycursor.description]
    json_data_2 = []
    for row in exit_log:
        json_data_2.append(dict(zip(row_headers, row)))

    json_data = {
        "entries": json_data_1,
        "exits": json_data_2
    }

    return json_data


# gets entire log from the DB
def get_full_log_from_database():
    sql = 'SELECT * FROM entry_sensor_tab'
    mycursor.execute(sql)
    entry_log = mycursor.fetchall()

    row_headers = [x[0] for x in mycursor.description]
    json_data_1 = []
    for row in entry_log:
        json_data_1.append(dict(zip(row_headers, row)))

    sql = 'SELECT * FROM exit_sensor_tab'
    mycursor.execute(sql)
    exit_log = mycursor.fetchall()

    row_headers = [x[0] for x in mycursor.description]
    json_data_2 = []
    for row in exit_log:
        json_data_2.append(dict(zip(row_headers, row)))

    json_data = {
        "entries": json_data_1,
        "exits": json_data_2
    }

    return json_data
