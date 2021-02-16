import os
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

from models.bed import get_bed
from models.emergency import add_emergency

MIN_BPM = 60
MAX_BPM = 100
MIN_BODY_TEMPERATURE = 35
MAX_BODY_TEMPERATURE = 37.5
MIN_MIN_BODY_PRESSURE = 60
MAX_MIN_BODY_PRESSURE = 80
MIN_MAX_BODY_PRESSURE = 90
MAX_MAX_BODY_PRESSURE = 120
MIN_BLOOD_OXYGENATION = 95

vital_data_blueprint = Blueprint('vital_data', __name__)

@vital_data_blueprint.route("/add", methods=["POST"]) #Add a new vital data
def add():
    fields = ["bpm", "body_temperature", "min_body_pressure", "max_body_pressure", "blood_oxygenation", "bed_id"]
    data = request.json

    for field in fields:
        if (not field in data):
            return abort(400)

    if (add_vital_data(data["bpm"], data["body_temperature"], data["min_body_pressure"], data["max_body_pressure"], data["blood_oxygenation"], data["bed_id"])):
        return jsonify({"message": "OK"})
    else:
        return abort(500)

@vital_data_blueprint.route("/") #Get latest vital data
def get_latest():
    inmate_id = request.args.get("inmate_id", default = None, type = int)
    if (inmate_id is not None):
        result = get_latest_vital_data(inmate_id)
        if (result is not None):
            return jsonify(result)
        else:
            return abort(500)
    else:
        return abort(400)

@vital_data_blueprint.route("/series/", methods=["GET"])
def get_series():
    inmate_id = request.args.get("inmate_id", default=None, type=int)
    field = request.args.get("field", default=None, type=str)
    start = request.args.get("start", default=None, type=str)
    end = request.args.get("end", default=None, type=str)

    if (inmate_id is not None) and (field is not None):
        result = get_vital_data_series(inmate_id, field, start, end)
        if (result is not None):
            return jsonify({"values" : result})
        else:
            return abort(500)
    else:
        return abort(400)



def add_vital_data(bpm: int, temperature: float, min_pressure: int, max_pressure: int, oxygen: int, bed_id: int) -> bool:
    try:
        bed = get_bed(bed_id)
        if (bed is not None):
            inmate_id = bed["inmate_id"]
            database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
            cursor = database.cursor()

            values = (bpm, temperature, min_pressure, max_pressure, oxygen, inmate_id)
            sql = ("""INSERT INTO vital_signs (tmstp, bpm, body_temperature, min_body_pressure, max_body_pressure, blood_oxygenation, inmate_id) VALUES (NOW(), %d, %0.1f, %d, %d, %d, %d)""" % values)
            cursor.execute(sql)
            database.commit()

            id = cursor.lastrowid
            database.close()

            emergency_flag = False
            emergency_string = []
            if ((bpm < MIN_BPM) and (bpm > 0)):
                emergency_flag = True
                emergency_string.append("bpm-")
            if (bpm > MAX_BPM) :
                emergency_flag = True
                emergency_string.append("bpm+")
            if ((temperature < MIN_BODY_TEMPERATURE) and (temperature > 0)):
                emergency_flag = True
                emergency_string.append("temperature-")
            if (temperature > MAX_BODY_TEMPERATURE):
                emergency_flag = True
                emergency_string.append("temperature+")
            if ((min_pressure < MIN_MIN_BODY_PRESSURE) and (min_pressure > 0)):
                emergency_flag = True
                emergency_string.append("min_pressure-")
            if (min_pressure > MAX_MIN_BODY_PRESSURE):
                emergency_flag = True
                emergency_string.append("min_pressure+")
            if ((max_pressure < MIN_MAX_BODY_PRESSURE) and (max_pressure > 0)):
                emergency_flag = True
                emergency_string.append("max_pressure-")
            if (max_pressure > MAX_MAX_BODY_PRESSURE):
                emergency_flag = True
                emergency_string.append("max_pressure+")
            if ((oxygen < MIN_BLOOD_OXYGENATION) and (oxygen > 0)):
                emergency_flag = True
                emergency_string.append("oxygenation-")
            
            if (emergency_flag):
                tags = ';'.join(emergency_string)
                return add_emergency(0, 1, tags, None, id, bed_id)
            else:
                return True
        else:
            return False
    except Exception as e:
        print(e)
        if (database.is_connected()):
            database.close()
        return False

def get_latest_vital_data(inmate_id: int) -> dict:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()

        val = (inmate_id)
        cursor.execute("SELECT inmate_vital_signs.id, tmstp, bpm, body_temperature, min_body_pressure, max_body_pressure, blood_oxygenation, inmate_vital_signs.inmate_id, name, surname, cf, date_birth, bed.id AS bed_id FROM bed INNER JOIN (SELECT last_vital_signs.id, tmstp, bpm, body_temperature, min_body_pressure, max_body_pressure, blood_oxygenation, inmate_id, name, surname, cf, date_birth FROM inmate INNER JOIN last_vital_signs ON inmate.id = last_vital_signs.inmate_id) AS inmate_vital_signs ON bed.inmate_id = inmate_vital_signs.inmate_id WHERE inmate_vital_signs.inmate_id = %d" % val)
        columns = [column[0] for column in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))
        
        inmate_v_s = data[0]
        vital_signs = {'id' : inmate_v_s['id'], 'tmstp' : inmate_v_s['tmstp'], 'bpm' : inmate_v_s['bpm'], 'body_temperature' : inmate_v_s['body_temperature'], 'min_body_pressure' : inmate_v_s['min_body_pressure'], 'max_body_pressure' : inmate_v_s['max_body_pressure'], 'blood_oxygenation' : inmate_v_s['blood_oxygenation']}
        inmate = {'id': inmate_v_s['inmate_id'], 'name': inmate_v_s['name'], 'surname': inmate_v_s['surname'], 'cf' : inmate_v_s['cf'], 'date_birth' : inmate_v_s['date_birth'], 'vital_signs' : vital_signs}

        database.close()
        return inmate
    except Exception as e:
        print(e)
        if (database.is_connected()):
            database.close()
        return None

def get_vital_data_series(inmate_id: int, field: str, start: str, end: str) -> list:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()

        if (field == "pressure"):
            field = "min_body_pressure, max_body_pressure"
    
        if (start != None and end != None):
            sql = ("""SELECT %s, tmstp FROM pepperiot.vital_signs WHERE inmate_id = %d AND tmstp BETWEEN "%s" AND "%s";""" % (field, inmate_id, start, end))
        else:
            sql = ("""SELECT %s, tmstp FROM pepperiot.vital_signs WHERE inmate_id = %d AND tmstp > DATE_SUB(NOW(), INTERVAL 2 MONTH) AND tmstp <= NOW();""" % (field, inmate_id))
        cursor.execute(sql)

        columns = [column[0] for column in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))

        series = []
        for element in data:
            tmstp = element["tmstp"]
            hour = ("%s:%s" % (tmstp.hour, tmstp.minute))
            if field != "min_body_pressure, max_body_pressure":
                series.append({"hour": hour, "value": element[field]})
            else:
                series.append({"hour": hour, "value_min": element["min_body_pressure"], "value_max": element["max_body_pressure"]})

        database.close()
        return series
    except Exception as e:
        print(e)
        if (database.is_connected):
            database.close()
        return None