import os
import constants
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort
from mysql.connector.errors import IntegrityError

class Room:
    def __init__(self, id : int, name : str):
        self.id = id
        self.name = name

    def add_room(self, data):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()

            self.name = (data["name"])
            sql = ("""INSERT INTO room (name_room) VALUES ("%s")""" % self.name)
            cursor.execute(sql)
            mydb.commit()

            return 200
        except IntegrityError:
            return 400
        except Exception:
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()

    def get_rooms_list(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()

            cursor.execute("SELECT * FROM room ORDER BY id")
            room_columns = [column[0] for column in cursor.description]
            room_list = []
            for row in cursor.fetchall():
                room_list.append(dict(zip(room_columns, row)))

            return room_list
        except Exception:
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()
    
    def get_all_rooms(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM room INNER JOIN (SELECT bed.id AS bed_id, bed.inmate_id, inmate.name, inmate.surname, bed.room_id FROM bed INNER JOIN inmate ON bed.inmate_id = inmate.id) AS bed_inmate ON room.id = bed_inmate.room_id")
            room_columns = [column[0] for column in cursor.description]
            room_list = []
            for row in cursor.fetchall():
                room_list.append(dict(zip(room_columns, row)))

            return room_list
        except:
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()

room_blueprint = Blueprint('room', __name__)

@room_blueprint.route("/add", methods=["POST"]) #Add a new room
def add():
    if(request.json is not None):
        if("name" in request.json):
            obj = Room(None, None)
            value = obj.add_room(request.json)
            if(value == 200):
                return jsonify({"message" : "ok"})
            else:
                return abort(value)
        else:
            return abort(400)
    else:
        return abort(400)


@room_blueprint.route("/list", methods=["GET"]) #Get list of all avaible rooms
def get_list():
    obj = Room(None, None)
    value = obj.get_rooms_list()
    if(value != 500):
        return jsonify(value)
    else:
        return abort(value)

@room_blueprint.route("/all", methods=["GET"]) #Get list of all avaible rooms with beds and inmates
def get_all():
    obj = Room(None, None)
    value = obj.get_all_rooms()
    if(value != 500):
        return jsonify(value)
    else:
        return abort(value)
