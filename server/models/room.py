from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort
import mysql.connector
from mysql.connector.errors import Error, IntegrityError
import constants

class Room:
    def __init__(self, id : int, name : str):
        self.id = id
        self.name = name

room_blueprint = Blueprint('room', __name__)

@room_blueprint.route("/add", methods=["POST"]) #Add a new room
def add():
    if(request.json is not None):
        if("name" in request.json):
            value = add_room(request.json)
            if(value == 200):
                return jsonify({"message" : "ok"})
            else:
                return abort(value)
        else:
            return abort(400)
    else:
        return abort(400)

def add_room(data):
    mydb = None
    try:
        mydb = mysql.connector.connect(
            user=constants.USER_DB,
            database=constants.DATABASE,
            password=constants.PASSWORD
        )
        cursor = mydb.cursor()

        val = (data["name"])
        sql = ("""INSERT INTO room (name_room) VALUES ("%s")""" % val)
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


@room_blueprint.route("/all", methods=["GET"]) #Get list of all avaible rooms
def get_all():
    value = get_rooms_list()
    if(value is not 500):
        return jsonify(value)
    else:
        return abort(value)

def get_rooms_list():
    mydb = None
    try:
        mydb = mysql.connector.connect(
            user=constants.USER_DB,
            database=constants.DATABASE,
            password=constants.PASSWORD
        )
        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM room")
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