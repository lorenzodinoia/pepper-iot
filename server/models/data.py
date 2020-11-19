from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort
from flask import json
import mysql.connector
import constants

class Data:
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
            self.vox = 0
            self.degree = 0
            self.humidity = 0
            self.room_id = None
            if("lux" in data):
                self.lux = data["lux"]
            if("vox" in data):
                self.vox = data["vox"]
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
                user=constants.USER_DB,
                database=constants.DATABASE,
                password=constants.PASSWORD
                )
                cursor = mydb.cursor()

                val = (self.lux, self.vox, self.degree, self.humidity, self.room_id)
                sql = ("""INSERT INTO data_iot (tmstp, lux, vox, degree, humidity, room_id) VALUES (NOW(), %d, %d, %d, %d, %d)""" % val)
                
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




data_blueprint = Blueprint('data', __name__)

@data_blueprint.route("/add", methods=["POST"]) #Add a new record
def add():
    data = request.json
    obj = Data(None, None, None, None, None, None, None)
    value = obj.add_data(data)
    if(value == 200):
        return jsonify({"message" : "ok"})
    else:
        return abort(value)
