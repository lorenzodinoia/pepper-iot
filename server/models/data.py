from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort
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

data_blueprint = Blueprint('data', __name__)

@data_blueprint.route("/add", methods=["POST"]) #Add a new record
def add():
    data = request.json
    if(data is not None):
        lux = 0
        vox = 0
        degree = 0
        humidity = 0
        room_id = None
        if("lux" in data):
            lux = data["lux"]
        if("vox" in data):
            vox = data["vox"]
        if("degree" in data):
            degree = data["degree"]
        if("humidity"in data):
            humidity = data["humidity"]
        if("room_id" in data):
            room_id = data["room_id"]
        else:
            return abort(400)

        mydb = None
        try:
            mydb = mysql.connector.connect(
            user=constants.USER_DB,
            database=constants.DATABASE,
            password=constants.PASSWORD
            )
            cursor = mydb.cursor()

            val = (lux, vox, degree, humidity, room_id)
            sql = ("""INSERT INTO data_iot (tmspt, lux, vox, degree, humidity, room_id) VALUES (NOW(), %d, %d, %d, %d, %d)""" % val)
            
            cursor.execute(sql)
            mydb.commit()

            return jsonify({"message" : "ok"})
        except:
            return abort(500)
        finally:
            if(mydb.is_connected()):
                mydb.close()
    else:
        return abort(400)

