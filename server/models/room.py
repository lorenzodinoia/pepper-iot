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
        try:
            mydb = mysql.connector.connect(
                user=constants.USER_DB,
                database=constants.DATABASE,
                password=constants.PASSWORD
            )
            cursor = mydb.cursor()

            data = request.json
            val = (data["name"])
            sql = ("""INSERT INTO room (name_room) VALUES ("%s")""" % val)
            cursor.execute(sql)
            mydb.commit()

            return jsonify({"message": "OK"})
        except IntegrityError:
            return jsonify({"message" : "Integrity violation"})
        except Exception:
            return abort(500)
        finally:
            if(mydb.is_connected()):
                mydb.close()
    else:
        return abort(400)

@room_blueprint.route("/all", methods=["GET"])
def get_all():
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

        return jsonify(room_list)

    except Exception:
        return abort(500)
    finally:
        if(mydb.is_connected()):
            mydb.close()

