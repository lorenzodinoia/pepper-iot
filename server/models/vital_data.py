import os
import constants
import mysql.connector
from flask import Blueprint
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
