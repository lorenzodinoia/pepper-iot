import os
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

from models.emergency import add_emergency

MIN_LUX = 401
MAX_LUX = 1000
MAX_VOC = 0.7
MIN_DEGREE = 15
MAX_DEGREE = 30
MAX_HUMIDITY = 60

env_data_blueprint = Blueprint('env_data', __name__)

@env_data_blueprint.route("/add", methods=["POST"]) #Add a new record
def add():
    fields = ["room_id", "lux", "voc", "degree", "humidity"]
    data = request.json

    for field in fields:
        if (not field in data):
            return abort(400)

    if (add_env_data(data["room_id"], data["lux"], data["voc"], data["degree"], data["humidity"])):
        return jsonify({"message" : "OK"})
    else:
        return abort(500)

@env_data_blueprint.route("/")
def get_latest():
    result = get_latest_env_data()
    if(result is not None):
        return jsonify(result)
    else:
        return abort(500)

@env_data_blueprint.route("/series/", methods=["GET"])
def get_series():
    room_id = request.args.get("room_id", default=None, type=int)
    field = request.args.get("field", default=None, type=str)
    start = request.args.get("start", default=None, type=str)
    end = request.args.get("end", default=None, type=str)

    if (room_id is not None) and (field is not None):
        result = get_env_data_series(room_id, field, start, end)
        if(result is not None):
            return jsonify({"values" : result})
        else:
            return abort(500)
    else:
        return abort(400)



def add_env_data(room_id: int, lux: int, voc: float, degree: float, humidity: int) -> bool:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()

        values = (lux, voc, degree, humidity, room_id)
        sql = ("""INSERT INTO environmental_data (tmstp, lux, voc, degree, humidity, room_id) VALUES (NOW(), %d, %0.1f, %d, %d, %d)""" % values)
        cursor.execute(sql)
        database.commit()
        id = cursor.lastrowid
        database.close()

        emergency_flag = False
        emergency_string = []
        if ((lux < MIN_LUX) and (lux > 0)):
            emergency_flag = True
            emergency_string.append("lux-")
        if (lux > MAX_LUX):
            emergency_flag = True
            emergency_string.append("lux+")
        if (voc > MAX_VOC):
            emergency_flag = True
            emergency_string.append("voc+")
        if (humidity > MAX_HUMIDITY):
            emergency_flag = True
            emergency_string.append("humidity+")
        if ((degree < MIN_DEGREE) and (degree > 0)):
            emergency_flag = True
            emergency_string.append("degree-")
        if (degree > MAX_DEGREE):
            emergency_flag = True
            emergency_string.append("degree+")

        if (emergency_flag):
            tags = ';'.join(emergency_string)
            return add_emergency(0, 0, tags, id, None, None)
        else:
            return True
    except Exception as e:
        print(e)
        if (database.is_connected()):
            database.close()
        return False

def get_latest_env_data() -> list:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()

        cursor.execute("SELECT * FROM latest_env_data")
        columns = [column[0] for column in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))

        room_list = []
        for element in data:
            env_data = {'id' : element['id'], 'tmstp' : element['tmstp'], 'lux' : element['lux'], 'voc' : element['voc'], 'degree' : element['degree'], 'humidity' : element['humidity']}
            room = {'id' : element['room_id'], 'name' : element['name_room'], 'env_data' : env_data}
            room_list.append(room)

        database.close()
        return room_list
    except Exception as e:
        print(e)
        if (database.is_connected()):
            database.close()
        return None

def get_env_data_series(room_id: int, field: str, start: str, end: str) -> list:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()

        if (start != None and end != None):
            sql = """SELECT %s, tmstp FROM pepperiot.environmental_data WHERE room_id = %d AND tmstp BETWEEN "%s" AND "%s";""" % (field, room_id, start, end)
        else:
            sql = """SELECT %s, tmstp FROM pepperiot.environmental_data WHERE room_id = %d AND tmstp > DATE_SUB(NOW(), INTERVAL 2 MONTH) AND tmstp <= NOW();""" % (field, room_id)

        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))

        series = []
        for element in data:
            tmstp = element["tmstp"]
            hour = ("%s:%s" % (tmstp.hour, tmstp.minute))
            series.append({"hour": hour, "value": element[field]})

        database.close()
        return series
    except Exception as e:
        print(e)
        if (database.is_connected()):
            database.close()
        return None