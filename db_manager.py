import mysql.connector as mysql

# connect to database
mydb = mysql.connect(
    host='localhost',
    user='root',
    passwd='sdpass',
    database='ENTRY_SENSOR_TAB'
)


# inserts a new entry to the respective table in the DB
def insert_entry_to_database(datetime, n_cars):
    mycursor = mydb.cursor()
    sql = "INSERT INTO ENTRY_SENSOR_TAB (DATETIME, NUM_CARS) VALUES (%s, %s)"
    val = (datetime, n_cars)

    mycursor.execute(sql, val)
    mydb.commit()


# inserts a new exit to the respective table in the DB
def insert_exit_to_database(datetime, n_cars):
    mycursor = mydb.cursor()
    sql = "INSERT INTO EXIT_SENSOR_TAB (DATETIME, NUM_CARS) VALUES (%s, %s)"
    val = (datetime, n_cars)

    mycursor.execute(sql, val)
    mydb.commit()
