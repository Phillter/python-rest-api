from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

class Employees(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from employees")
        return {'employees' :[i[0] for i in query.cursor.fetchall()]}

class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks")
        result = {'data': [dict(zip(tuple( query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class Tracks_Name(Resource):
    def get(self, track_id):
        conn = db_connect.connect()
        query = conn.execute("select tracks.name as Track, artists.name as Artist, albums.title as Album \
        from tracks \
        inner join artists on artists.artistid = albums.artistid\
        inner join albums on tracks.AlbumId = albums.AlbumId \
        where TrackId ={}".format(track_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        print result
        return jsonify(result)

class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId ={}".format(employee_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Employees, "/employees")
api.add_resource(Tracks, "/tracks")
api.add_resource(Employees_Name, "/employees/<employee_id>")
api.add_resource(Tracks_Name, "/tracks/<track_id>")

if __name__ == '__main__':
    app.run(port='5002')