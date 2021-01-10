import os
import constants
import mysql.connector
from flask import Blueprint, json
from flask import request
from flask import jsonify
from flask import abort

class Vital_data:
    def __init__(self, id : int, tmstp : str, bpm : int, body_temperature : float, body_pressure : int, blood_oxygenation : int, inmate_id : int):
        self.id = id
        self.tmstp = tmstp
        self.bpm = bpm
        self.body_temperature = body_temperature
        self.body_pressure = body_pressure
        self.blood_oxygenation = blood_oxygenation
        self.inmate_id = inmate_id

    def add_data(self, data):
        if(data is not None):
            self.bpm = 0
            self.body_temperature = 0
            self.body_pressure = 0
            self.inmate_id = None
            if("bpm" in data):
                self.bpm = data["bpm"]
            if("body_temperature" in data):
                self.body_temperature = data["body_temperature"]
            if("body_pressure" in data):
                self.body_pressure = data["body_pressure"]
            if("blood_oxygenation" in data):
                self.blood_oxygenation = data["blood_oxygenation"]
            if("inmate_id" in data):
                self.inmate_id = data["inmate_id"]
            else:
                return 400

        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()

            val = (self.bpm, self.body_temperature, self.body_pressure, self.blood_oxygenation, self.inmate_id)
            sql = ("""INSERT INTO vital_signs (tmstp, bpm, body_temperature, body_pressure, blood_oxygenation, inmate_id) VALUES (NOW(), %d, %0.1f, %d, %d, %d)""" % val)
                
            cursor.execute(sql)
            mydb.commit()

            self.id = cursor.lastrowid
                
            return 200
        except:
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()
            else:
                return 400
    
    def get_latest_data(self, room_id):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()

            val = (room_id)
            cursor.execute("SELECT inmate_vital_signs.id, tmstp, bpm, body_temperature, body_pressure, blood_oxygenation, inmate_vital_signs.inmate_id, name, surname, cf, date_birth, bed.id AS bed_id FROM bed INNER JOIN (SELECT last_vital_signs.id, tmstp, bpm, body_temperature, body_pressure, blood_oxygenation, inmate_id, name, surname, cf, date_birth FROM inmate INNER JOIN last_vital_signs ON inmate.id = last_vital_signs.inmate_id) AS inmate_vital_signs ON bed.inmate_id = inmate_vital_signs.inmate_id WHERE bed.room_id = %d" % val)
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
            return data
        except Exception as e:
            print(e)
            return 500
        finally:
            if mydb.is_connected():
                mydb.close()

vital_data_blueprint = Blueprint('vital_data', __name__)

@vital_data_blueprint.route("/add", methods=["POST"]) #Add a new vital data
def add():
    data = request.json
    obj = Vital_data(None, None, None, None, None, None, None)
    value = obj.add_data(data)
    if(value == 200):
        return jsonify({"message" : "ok"})
    else:
        return abort(value)

@vital_data_blueprint.route("/")
def get_latest():
    room_id = request.args.get("room_id", default=None, type=int)
    if(room_id is not None):
        obj = Vital_data(None, None, None, None, None, None, None)
        value = obj.get_latest_data(room_id)
        if(value != 500):
            return jsonify(value)
        else:
            return abort(400)
    else:
        return abort(400)