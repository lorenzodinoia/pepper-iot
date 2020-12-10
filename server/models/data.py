import os
import constants
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort
from flask import json

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
                sql = ("""INSERT INTO data_iot (tmstp, lux, voc, degree, humidity, room_id) VALUES (NOW(), %d, %d, %0.1f, %d, %d)""" % val)
                
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

@data_blueprint.route("/")
def get_latest():
    try:
        mydb = mysql.connector.connect(
            user = os.getenv("DATABASE_USER"),
            database = os.getenv("DATABASE_NAME"),
            password = os.getenv("DATABASE_PASSWORD")
        )
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM room INNER JOIN data_iot ON room.id = data_iot.room_id WHERE data_iot.id IN (SELECT MAX(id) FROM pepperiot.data_iot GROUP BY room_id)")
        columns = [column[0] for column in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))
        return jsonify(data)
    except Exception:
        return abort(500)
    finally:
        if mydb.is_connected():
            mydb.close()