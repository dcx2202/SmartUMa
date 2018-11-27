import mysql.connector as mysql

# connect to database
mydb = mysql.connect(
    host='localhost',
    user='root',
    passwd='sdpass',
    database='smart_uma_parking_sensors_db'
)


# inserts a new entry to the respective table in the DB
def insert_entry_to_database(date, time, n_cars):
    mycursor = mydb.cursor()
    sql = "INSERT INTO entry_sensor_tab (date, time, num_cars) VALUES (%s, %s, %s)"
    val = (date, time, n_cars)

    mycursor.execute(sql, val)
    mydb.commit()


# inserts a new exit to the respective table in the DB
def insert_exit_to_database(date, time, n_cars):
    mycursor = mydb.cursor()
    sql = "INSERT INTO exit_sensor_tab (date, time, num_cars) VALUES (%s, %s, %s)"
    val = (date, time, n_cars)

    mycursor.execute(sql, val)
    mydb.commit()
