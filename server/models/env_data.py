import os
import mysql.connector
from models.emergency import Emergency
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

MIN_LUX = 401
MAX_LUX = 1000
MAX_VOC = 0.7
MIN_DEGREE = 15
MAX_DEGREE = 30
MAX_HUMIDITY = 60

class Environmental_data:
    def __init__(self, id : int, timestamp : str, lux : int, voc : int, degree : int, humidity : int, room_id : int):
        self.id = id
        self.timestamp = timestamp
        self.lux = lux
        self.voc = voc
        self.degree = degree
        self.humidity = humidity
        self.room_id = room_id

    def add_data(self, data):
        if(data is not None):
            self.lux = 0
            self.voc = 0
            self.degree = 0
            self.humidity = 0
            self.room_id = None
            if("lux" in data):
                self.lux = data["lux"]
            if("voc" in data):
                self.voc = data["voc"]
            if("degree" in data):
                self.degree = data["degree"]
            if("humidity" in data):
                self.humidity = data["humidity"]
            if("room_id" in data):
                self.room_id = data["room_id"]
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

                val = (self.lux, self.voc, self.degree, self.humidity, self.room_id)
                print("qui")
                sql = ("""INSERT INTO environmental_data (tmstp, lux, voc, degree, humidity, room_id) VALUES (NOW(), %d, %0.1f, %d, %d, %d)""" % val)
                cursor.execute(sql)
                mydb.commit()
                print("qui")
                self.id = cursor.lastrowid

            except Exception as e:
                print(e)
                return 500
            finally:
                if(mydb.is_connected()):
                    mydb.close()
            
            emergency_flag = False
            if(self.lux < MIN_LUX):
                emergency_flag = True
            if(self.lux > MAX_LUX):
                emergency_flag = True
            if(self.voc > MAX_VOC):
                emergency_flag = True
            if(self.degree < MIN_DEGREE):
                emergency_flag = True
            if(self.degree > MAX_DEGREE):
                emergency_flag = True
            if(self.humidity < MAX_DEGREE):
                emergency_flag = True

            if(emergency_flag):
                emergency_obj = Emergency(None, None, None, None, None, None, None, None)
                print(self.id)
                data = {"level_em" : 0, "type_em" : 0, "env_data_id" : self.id}
                value = emergency_obj.add_emergency(data)
                if(value != 200):
                    return 500
            
            return 200
        else:
            return 400

    def get_latest_data(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()
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

            return room_list
        except:
            return 500
        finally:
            if mydb.is_connected():
                mydb.close()




env_data_blueprint = Blueprint('env_data', __name__)

@env_data_blueprint.route("/add", methods=["POST"]) #Add a new record
def add():
    data = request.json
    obj = Environmental_data(None, None, None, None, None, None, None)
    value = obj.add_data(data)
    if(value == 200):
        return jsonify({"message" : "ok"})
    else:
        return abort(value)

@env_data_blueprint.route("/")
def get_latest():
    obj = Environmental_data(None, None, None, None, None, None, None)
    value = obj.get_latest_data()
    if(value != 500):
        return jsonify(value)
    else:
        return abort(value)