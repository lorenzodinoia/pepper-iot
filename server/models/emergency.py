from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort
from flask import json
import mysql.connector
from models.data import Data
import constants

class Emergency:
    def __init__(self, id : int ,timestamp : str, room_id : int, data_id : int):
        self.id = id
        self.timestamp = timestamp
        self.room_id = room_id
        self.data_id = data_id
    
    def save_emergency(self, room_id, data_id):
        mydb = None
        try:
            mydb = mysql.connector.connect(
            user = constants.USER_DB,
            database = constants.DATABASE,
            password = constants.PASSWORD
            )
            cursor = mydb.cursor()

            val = (room_id, data_id)
            sql = ("""INSERT INTO emergency (tmstp, room_id, data_id) VALUES (NOW(), %d, %d)""" % val)
            
            cursor.execute(sql)
            mydb.commit()

            return 200
        except:
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()

    def get_first_emergency(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = constants.USER_DB,
                database = constants.DATABASE,
                password = constants.PASSWORD
                )
            cursor = mydb.cursor()

            sql = "SELECT * FROM emergency ORDER BY tmstp ASC LIMIT 1"

            cursor.execute(sql)

            emergency_columns = [column[0] for column in cursor.description]
            emergency_list = []
            for row in cursor.fetchall():
                emergency_list.append(dict(zip(emergency_columns, row)))

            mydb.commit()
            return emergency_list
        except:
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()
    
    def delete_emergency(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = constants.USER_DB,
                database = constants.DATABASE,
                password = constants.PASSWORD
            )
            cursor = mydb.cursor()

            val = self.id
            sql = ("""DELETE FROM emergency WHERE id = %d""" % val)

            cursor.execute(sql)

            mydb.commit()

            return 200
        except:
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()


emergency_blueprint = Blueprint('emergency', __name__)

@emergency_blueprint.route("/add", methods=["POST"]) #Add a new emergency call
def add():
    data = request.json
    obj = Data(None, None, None, None, None, None, None)
    value = obj.add_data(data)
    if(value == 200):
        emergency = Emergency(None, None, None, None)
        room_id = obj.room_id
        data_id = obj.id
        value = emergency.save_emergency(room_id, data_id)
        if(value == 200):
            return jsonify({"message" : "ok"})
        else:
            return abort(value)
    else:
        return abort(value)

@emergency_blueprint.route("/first", methods=["GET"]) #Return the first emergency call
def first():
    emergency = Emergency(None, None, None, None)
    values = emergency.get_first_emergency()
    if(values is not 500):
        return jsonify(values)
    else:
        return abort(values)

@emergency_blueprint.route("/delete/<int:id>", methods=["DELETE"]) #Delete the emergency call
def delete(id : int):
    emergency = Emergency(id, None, None, None)
    value = emergency.delete_emergency()
    if(value == 200):
        return jsonify({"message" : "ok"})
    else:
        return abort(value)
