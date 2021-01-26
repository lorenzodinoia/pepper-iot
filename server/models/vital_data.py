import os
from re import T
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort
from models.emergency import Emergency


MIN_BPM = 60
MAX_BPM = 100
MIN_BODY_TEMPERATURE = 35
MAX_BODY_TEMPERATURE = 37.5
MAX_MIN_BODY_PRESSURE = 80
MAX_MAX_BODY_PRESSURE = 120
MIN_BLOOD_OXYGENATION = 95


class Vital_data:
    def __init__(self, id : int, tmstp : str, bpm : int, body_temperature : float, min_body_pressure : int, max_body_pressure : int, blood_oxygenation : int, inmate_id : int):
        self.id = id
        self.tmstp = tmstp
        self.bpm = bpm
        self.body_temperature = body_temperature
        self.min_body_pressure = min_body_pressure
        self.max_body_pressure = max_body_pressure
        self.blood_oxygenation = blood_oxygenation
        self.inmate_id = inmate_id

    def add_data(self, data):
        print(data)
        if(data is not None):
            self.bpm = 0
            self.body_temperature = 0
            self.min_body_pressure = 0
            self.max_body_pressure = 0
            self.blood_oxygenation = 0
            self.inmate_id = None
            if("bpm" in data):
                self.bpm = data["bpm"]
            if("body_temperature" in data):
                self.body_temperature = data["body_temperature"]
            if("min_body_pressure" in data):
                self.min_body_pressure = data["min_body_pressure"]
            if("max_body_pressure" in data):
                self.max_body_pressure = data["max_body_pressure"]
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

                val = (self.bpm, self.body_temperature, self.min_body_pressure, self.max_body_pressure, self.blood_oxygenation, self.inmate_id)
                sql = ("""INSERT INTO vital_signs (tmstp, bpm, body_temperature, min_body_pressure, max_body_pressure, blood_oxygenation, inmate_id) VALUES (NOW(), %d, %0.1f, %d, %d, %d, %d)""" % val)
                cursor.execute(sql)
                mydb.commit()

                self.id = cursor.lastrowid
                    
            except Exception as e:
                print(e)
                return 500
            finally:
                if(mydb.is_connected()):
                    mydb.close()
                else:
                    return 400
            
            emergency_flag = False
            if(self.bpm < MIN_BPM):
                if(self.bpm > 0):
                    emergency_flag = True
            if(self.bpm > MAX_BPM):
                emergency_flag = True
            if(self.body_temperature < MIN_BODY_TEMPERATURE):
                if(self.body_temperature > 0):
                    emergency_flag = True
            if(self.body_temperature > MAX_BODY_TEMPERATURE):
                emergency_flag = True
            if(self.min_body_pressure > MAX_MIN_BODY_PRESSURE):
                emergency_flag = True
            if(self.max_body_pressure > MAX_MAX_BODY_PRESSURE):
                emergency_flag = True
            if(self.blood_oxygenation < MIN_BLOOD_OXYGENATION):
                if(self.blood_oxygenation > 0):
                    emergency_flag = True
            
            if(emergency_flag):
                emergency_obj = Emergency(None, None, None, None, None, None, None, None)
                data = {"level_em" : 0, "type_em" : 1, "vital_signs_id" : self.id}
                value = emergency_obj.add_emergency(data)
                if(value != 200):
                    return 500

            return 200
        else:
            return 500
    
    def get_latest_data(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()

            val = (self.inmate_id)
            cursor.execute("SELECT inmate_vital_signs.id, tmstp, bpm, body_temperature, min_body_pressure, max_body_pressure, blood_oxygenation, inmate_vital_signs.inmate_id, name, surname, cf, date_birth, bed.id AS bed_id FROM bed INNER JOIN (SELECT last_vital_signs.id, tmstp, bpm, body_temperature, min_body_pressure, max_body_pressure, blood_oxygenation, inmate_id, name, surname, cf, date_birth FROM inmate INNER JOIN last_vital_signs ON inmate.id = last_vital_signs.inmate_id) AS inmate_vital_signs ON bed.inmate_id = inmate_vital_signs.inmate_id WHERE inmate_vital_signs.inmate_id = %d" % val)
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
            
            inmate_v_s = data[0]
            vital_signs = {'id' : inmate_v_s['id'], 'tmstp' : inmate_v_s['tmstp'], 'bpm' : inmate_v_s['bpm'], 'body_temperature' : inmate_v_s['body_temperature'], 'min_body_pressure' : inmate_v_s['min_body_pressure'], 'max_body_pressure' : inmate_v_s['max_body_pressure'], 'blood_oxygenation' : inmate_v_s['blood_oxygenation']}
            inmate = {'id': inmate_v_s['inmate_id'], 'name': inmate_v_s['name'], 'surname': inmate_v_s['surname'], 'cf' : inmate_v_s['cf'], 'date_birth' : inmate_v_s['date_birth'], 'vital_signs' : vital_signs}

            return inmate
        except:
            return 500
        finally:
            if mydb.is_connected():
                mydb.close()

vital_data_blueprint = Blueprint('vital_data', __name__)

@vital_data_blueprint.route("/add", methods=["POST"]) #Add a new vital data
def add():
    data = request.json
    obj = Vital_data(None, None, None, None, None, None, None, None)
    print(data)
    value = obj.add_data(data)
    if(value == 200):
        return jsonify({"message" : "ok"})
    else:
        return abort(value)

@vital_data_blueprint.route("/") #Get latest vital data
def get_latest():
    inmate_id = request.args.get("inmate_id", default=None, type=int)
    if(inmate_id is not None):
        obj = Vital_data(None, None, None, None, None, None, None, inmate_id)
        value = obj.get_latest_data()
        if(value != 500):
            return jsonify(value)
        else:
            return abort(400)
    else:
        return abort(400)