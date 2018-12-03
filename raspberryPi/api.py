from flask import Flask, jsonify, json, request
from flask_restful import Resource, Api
import datetime
import db_manager
import raspbpi

app = Flask(__name__)
api = Api(app)


# Helper functions
def calculate_average_number_cars_parked_today():
    spaces = get_number_cars_by_hour()
    sum = 0

    # Average only the active hours - 05h:00m -> 22h:00m
    for i in range(6, 22):
        sum += spaces[i]

    current_hour = datetime.datetime.now().hour

    # Divide the sum by the number of active hours that have passed today (including the current hour)
    if current_hour < 5:
        return 0
    elif current_hour < 22:
        return sum / (datetime.datetime.now().hour - 4)
    elif current_hour < 24:
        return sum / 17


def get_number_cars_by_hour():
    # get full last 24 hours log
    last24hlog = json.loads(db_manager.get_last_24h_log_from_database().get_data())

    # get only today's log
    for i in range(len(last24hlog['entries']) - 1, -1, -1):
        if int(last24hlog['entries'][i]['date'].split('-')[2]) != datetime.date.today().day:
            last24hlog['entries'].pop(i)

    for i in range(len(last24hlog['exits']) - 1, -1, -1):
        if int(last24hlog['exits'][i]['date'].split('-')[2]) != datetime.date.today().day:
            last24hlog['exits'].pop(i)

    # declare variables
    spaces = []
    entry_spaces = []
    exit_spaces = []
    entry_datetimes = []
    exit_datetimes = []

    # initializer variables
    for i in range(0, 24):
        spaces.append(0)
        entry_spaces.append(0)
        exit_spaces.append(0)
        entry_datetimes.append(0)
        exit_datetimes.append(0)

    # get last entry/exit date of each hour
    for i in range(0, len(last24hlog['entries'])):
        entry_datetimes[int(last24hlog['entries'][i]['time'].split(':')[0])] = last24hlog['entries'][i]['date'] + " " + \
                                                                               last24hlog['entries'][i]['time']

    for i in range(0, len(last24hlog['exits'])):
        exit_datetimes[int(last24hlog['exits'][i]['time'].split(':')[0])] = last24hlog['exits'][i]['date'] + " " + \
                                                                            last24hlog['exits'][i]['time']

    # get last number of cars parked at each hour from both entries and exits
    for i in range(0, len(last24hlog['entries'])):
        entry_spaces[int(last24hlog['entries'][i]['time'].split(':')[0])] = last24hlog['entries'][i]['num_cars']

    for i in range(0, len(last24hlog['exits'])):
        exit_spaces[int(last24hlog['exits'][i]['time'].split(':')[0])] = last24hlog['exits'][i]['num_cars']

    # for each hour create datetime objects, compare and store in spaces the last overall number of cars parked
    for i in range(0, 24):

        # create entry datetime object
        if entry_datetimes[i] == 0:
            entry_datetime = 0
        else:
            entry_date = entry_datetimes[i].split(' ')[0].split('-')
            entry_time = entry_datetimes[i].split(' ')[1].split(':')
            entry_datetime = datetime.datetime(int(entry_date[0]),
                                               int(entry_date[1]),
                                               int(entry_date[2]),
                                               int(entry_time[0]),
                                               int(entry_time[1]),
                                               int(entry_time[2].split('.')[0]),
                                               int(entry_time[2].split('.')[1]))

        # create exit datetime object
        if exit_datetimes[i] == 0:
            exit_datetime = 0
        else:
            exit_date = exit_datetimes[i].split(' ')[0].split('-')
            exit_time = exit_datetimes[i].split(' ')[1].split(':')
            exit_datetime = datetime.datetime(int(exit_date[0]),
                                              int(exit_date[1]),
                                              int(exit_date[2]),
                                              int(exit_time[0]),
                                              int(exit_time[1]),
                                              int(exit_time[2].split('.')[0]),
                                              int(exit_time[2].split('.')[1]))

        # check which one is the most recent
        if entry_datetime == 0 and exit_datetime == 0:
            spaces[i] = 0
        elif entry_datetime != 0 and exit_datetime == 0:
            spaces[i] = entry_spaces[i]
        elif entry_datetime == 0 and exit_datetime != 0:
            spaces[i] = exit_spaces[i]
        elif entry_datetime > exit_datetime:
            spaces[i] = entry_spaces[i]
        elif entry_datetime < exit_datetime:
            spaces[i] = exit_spaces[i]

    return spaces


def get_number_of_entries_today():
    # get full last 24 hours log
    last24hlog = json.loads(db_manager.get_last_24h_log_from_database().get_data())

    # get only today's entries
    for i in range(len(last24hlog['entries']) - 1, -1, -1):
        if int(last24hlog['entries'][i]['date'].split('-')[2]) != datetime.date.today().day:
            last24hlog['entries'].pop(i)

    return len(last24hlog['entries'])


def get_number_of_exits_today():
    # get full last 24 hours log
    last24hlog = json.loads(db_manager.get_last_24h_log_from_database().get_data())

    # get only today's exits
    for i in range(len(last24hlog['exits']) - 1, -1, -1):
        if int(last24hlog['exits'][i]['date'].split('-')[2]) != datetime.date.today().day:
            last24hlog['exits'].pop(i)

    return len(last24hlog['exits'])


def get_busiest_hours_today():
    spaces = get_number_cars_by_hour()
    busiest_hours = []
    max = max(spaces)

    for i in spaces:
        if spaces[i] == max:
            busiest_hours.append(i)

    return busiest_hours


def get_event_datetime(elem):
    entry_date = elem['date'].split('-')
    entry_time = elem['time'].split(':')
    event_datetime = datetime.datetime(int(entry_date[0]),
                                       int(entry_date[1]),
                                       int(entry_date[2]),
                                       int(entry_time[0]),
                                       int(entry_time[1]),
                                       int(entry_time[2].split('.')[0]),
                                       int(entry_time[2].split('.')[1]))

    return event_datetime


def get_activity_log():
    # get full last 24 hours log
    last24hlog = json.loads(db_manager.get_last_24h_log_from_database().get_data())

    # declare variables
    events = []
    entries = []
    exits = []

    # get last 8 entries and exits
    for i in range(0, 8):
        entries.append({"event_info": last24hlog['entries'][len(last24hlog) - 1 - i], "event_type": "entry"})
        exits.append({"event_info": last24hlog['exits'][len(last24hlog) - 1 - i], "event_type": "exit"})

    # join them
    temp_events = entries + exits

    # sort them by date
    sorted_events = sorted(temp_events, key=get_event_datetime)

    # remove the 8 least recent events out of the 16
    for i in range(8):
        sorted_events.pop(0)

    # for each event get the data we want and add it to the final list of events
    for i in range(5):
        # create event datetime object
        event_date = sorted_events[i]['event_info']['date'].split('-')
        event_time = sorted_events[i]['event_info']['time'].split(':')
        event_datetime = datetime.datetime(int(event_date[0]),
                                           int(event_date[1]),
                                           int(event_date[2]),
                                           int(event_time[0]),
                                           int(event_time[1]),
                                           int(event_time[2].split('.')[0]),
                                           int(event_time[2].split('.')[1]))

        # get string indicating how much time has passed since then
        time_str = get_event_string(event_datetime)

        # add to the final list of events a new event with a description of it and how long ago it happened
        if sorted_events[i]['event_type'] == "entry": # if it is an entry event the string should say so
            events.append({"event": "A car entered the park", "time": time_str})
        else: # if it is an exit event the string says so too
            events.append({"event": "A car exited the park", "time": time_str})

    return events


def get_event_string(entry_datetime):
    timedelta = datetime.datetime.now() - entry_datetime
    entry_time = timedelta.__str__().split(':')

    if int(entry_time[0]) != 0:
        time_str = entry_time[0] + " hours"
        if int(entry_time[1]) != 0:
            time_str = time_str + " and " + entry_time[1] + " minutes ago"
        else:
            time_str = time_str + " ago"
    elif int(entry_time[1]) != 0:
        time_str = entry_time[1] + " minutes ago"
    else:
        time_str = "just now"

    return time_str


# Request handling
class NumberOfCarsParked(Resource):
    def get(self):
        response = jsonify(db_manager.get_num_cars_parked_from_db())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class NumberOfEntriesInTheLastHour(Resource):
    def get(self):
        response = jsonify(db_manager.get_num_entries_last_hour_from_db())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class NumberOfExitsInTheLastHour(Resource):
    def get(self):
        response = jsonify(db_manager.get_num_exits_last_hour_from_db())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class NumberOfEntriesToday(Resource):
    def get(self):
        response = jsonify(get_number_of_entries_today())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class NumberOfExitsToday(Resource):
    def get(self):
        response = jsonify(get_number_of_exits_today())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class NumberOfSpaces(Resource):
    def get(self):
        response = jsonify(raspbpi.get_num_spaces())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class NumberOfFreeSpaces(Resource):
    def get(self):
        response = jsonify(db_manager.get_num_free_spaces_from_db())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class AverageNumberOfCarsParkedToday(Resource):
    def get(self):
        response = jsonify(calculate_average_number_cars_parked_today())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class AverageNumberOfFreeSpacesToday(Resource):
    def get(self):
        response = jsonify(raspbpi.get_num_spaces() - calculate_average_number_cars_parked_today())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class NumberOfCarsParkedTodayHourly(Resource):
    def get(self):
        response = jsonify(get_number_cars_by_hour())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class BusiestHoursToday(Resource):
    def get(self):
        response = jsonify(get_busiest_hours_today())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class ActivityLog(Resource):
    def get(self):
        response = jsonify(get_activity_log())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

class Statistics(Resource):
    def get(self):
        # response = jsonify(raspbpi.get_statistics())
        response = jsonify({"Number of cars parked": db_manager.get_num_cars_parked_from_db(),
                            "Number of free spaces": db_manager.get_num_free_spaces_from_db(),
                            "Number of spaces": raspbpi.get_num_spaces(),
                            "Number of entries in the last hour": db_manager.get_num_entries_last_hour_from_db(),
                            "Number of exits in the last hour": db_manager.get_num_exits_last_hour_from_db(),
                            "Number of entries today": get_number_of_entries_today(),
                            "Number of exits today": get_number_of_exits_today(),
                            "Average number of cars parked today": calculate_average_number_cars_parked_today(),
                            "Average number of free spaces today": raspbpi.get_num_spaces() - calculate_average_number_cars_parked_today(),
                            "Number of cars parked today hourly": get_number_cars_by_hour(),
                            "Busiest hours today": get_busiest_hours_today(),
                            "Activity log": get_activity_log()
                            })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class Last24HoursHistory(Resource):
    def get(self):
        response = db_manager.get_last_24h_log_from_database()
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class AllTimeHistory(Resource):
    def get(self):
        response = db_manager.get_full_log_from_database()
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


class ApiHelp(Resource):
    def get(self):
        response = "Available API paths: \n\n"
        response += "Number of cars parked: /number_of_cars_parked\n"
        response += "Number of cars parked today hourly: /number_of_cars_parked_today_hourly\n"
        response += "Number of entries in the last hour: /number_of_entries_in_the_last_hour\n"
        response += "Number of exits in the last hour: /number_of_exits_in_the_last_hour\n"
        response += "Number of entries today: /number_of_entries_today\n"
        response += "Number of exits today: /number_of_exits_today\n"
        response += "Number of spaces: /number_of_spaces\n"
        response += "Number of free spaces: /number_of_free_spaces\n"
        response += "Average number of cars parked today: /average_number_of_cars_parked_today\n"
        response += "Average number of free spaces today: /average_number_of_free_spaces_today\n"
        response += "Busiest hours today: /busiest_hours_today\n"
        response += "Activity log: /activity_log\n"
        response += "Statistics: /statistics\n"
        response += "Last 24 hours history: /last_24_hours_history\n"
        response += "All time history: /all_time_history"

        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


api.add_resource(ApiHelp, '/api_help')
api.add_resource(NumberOfCarsParked, '/number_of_cars_parked')
api.add_resource(NumberOfCarsParkedTodayHourly, '/number_of_cars_parked_today_hourly')
api.add_resource(NumberOfEntriesInTheLastHour, '/number_of_entries_in_the_last_hour')
api.add_resource(NumberOfExitsInTheLastHour, '/number_of_exits_in_the_last_hour')
api.add_resource(NumberOfEntriesToday, '/number_of_entries_today')
api.add_resource(NumberOfExitsToday, '/number_of_exits_today')
api.add_resource(NumberOfSpaces, '/number_of_spaces')
api.add_resource(NumberOfFreeSpaces, '/number_of_free_spaces')
api.add_resource(AverageNumberOfCarsParkedToday, '/average_number_of_cars_parked_today')
api.add_resource(AverageNumberOfFreeSpacesToday, '/average_number_of_free_spaces_today')
api.add_resource(BusiestHoursToday, '/busiest_hours_today')
api.add_resource(ActivityLog, '/activity_log')
api.add_resource(Statistics, '/statistics')
api.add_resource(Last24HoursHistory, '/last_24_hours_history')
api.add_resource(AllTimeHistory, '/all_time_history')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='25000', threaded=True)
