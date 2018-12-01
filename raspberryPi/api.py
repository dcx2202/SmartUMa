from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import db_manager
import raspbpi

app = Flask(__name__)
api = Api(app)


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


class Statistics(Resource):
    def get(self):
        # response = jsonify(raspbpi.get_statistics())
        response = jsonify({"Number of cars parked": db_manager.get_num_cars_parked_from_db(),
                            "Number of free spaces": db_manager.get_num_free_spaces_from_db(),
                            "Number of spaces": raspbpi.get_num_spaces(),
                            "Number of entries in the last hour": db_manager.get_num_entries_last_hour_from_db(),
                            "Number of exits in the last hour": db_manager.get_num_exits_last_hour_from_db()
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


api.add_resource(NumberOfCarsParked, '/number_of_cars_parked')
api.add_resource(NumberOfEntriesInTheLastHour, '/number_of_entries_in_the_last_hour')
api.add_resource(NumberOfExitsInTheLastHour, '/number_of_exits_in_the_last_hour')
api.add_resource(NumberOfSpaces, '/number_of_spaces')
api.add_resource(NumberOfFreeSpaces, '/number_of_free_spaces')
api.add_resource(Statistics, '/statistics')
api.add_resource(Last24HoursHistory, '/last_24_hours_history')
api.add_resource(AllTimeHistory, '/all_time_history')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='25000', threaded=True)
