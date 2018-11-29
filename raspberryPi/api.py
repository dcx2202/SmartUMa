from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class NumberOfCarsParked(Resource):
    def get(self):
        # return {"Number of cars parked": get_number_of_cars_parked_from_db()}
        return {"Number of cars parked": "es um pao"}


class NumberOfEntriesInTheLastHour(Resource):
    def get(self):
        # return {"Number of entries in the last hour": get_number_of_entries_in_the_last_hour_from_db()} - retorna json
        return


class NumberOfExitsInTheLastHour(Resource):
    def get(self):
        # return {"Number of exits in the last hour": get_number_of_exits_in_the_last_hour_from_db()}
        return


class NumberOfSpaces(Resource):
    def get(self):
        # return {"Number of spaces": get_number_of_spaces()}
        return


class Statistics(Resource):
    def get(self):
        # return {"Statistics": get_statistics()}
        return


class Last24HoursHistory(Resource):
    def get(self):
        # return {"Last 24 hours history": get_last_24_hours_history()}
        return


class AllTimeHistory(Resource):
    def get(self):
        # return {"All time history": get_all_time_history()}
        return


api.add_resource(NumberOfCarsParked, '/number_of_cars_parked')
api.add_resource(NumberOfEntriesInTheLastHour, '/number_of_entries_in_the_last_hour')
api.add_resource(NumberOfExitsInTheLastHour, '/number_of_exits_in_the_last_hour')
api.add_resource(NumberOfSpaces, '/number_of_spaces')
api.add_resource(Statistics, '/statistics')
api.add_resource(Last24HoursHistory, '/last_24_hours_history')
api.add_resource(AllTimeHistory, '/all_time_history')


if __name__ == '__main__':
    app.run(debug=False. host='192.168.1.156') #change host ip if raspberry is on a different network
