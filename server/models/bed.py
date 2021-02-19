import os
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

bed_blueprint = Blueprint('bed', __name__)

@bed_blueprint.route("/add", methods=["POST"]) #Add a new bed
def add():
    data = request.json
    if ((data is not None) and ("inmate_id" in data) and ("room_id" in data)):
        if (add_bed(data["inmate_id"], data["room_id"])):
            return jsonify({"message" : "OK"})
        else:
            return abort(500)
    else:
        return abort(400)

@bed_blueprint.route("/", methods=["GET"]) #Get bed from id
def get():
    bed_id = request.args.get("id", default=None, type=int)
    if (bed_id is not None):
        bed = get_bed(bed_id)
        if (bed is not None):
            return jsonify(bed)
        else:
            return abort(500)
    else:
        return abort(400)

@bed_blueprint.route("/all", methods=["GET"]) #Get the list of all beds in a room
def get_all():
    room_id = request.args.get("room_id", default=None, type=int)
    if (room_id is not None):
        beds = get_beds_list(room_id)
        if (beds is not None):
            return jsonify(beds)
        else:
            return abort(500)
    else:
        return abort(400)



def add_bed(inmate_id: int, room_id: int) -> bool:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()
        values = (inmate_id, room_id)
        sql = ("""INSERT INTO bed (inmate_id, room_id) VALUES (%d, %d)""" % values)
        cursor.execute(sql)
        database.commit()
        return True
    except Exception as e:
        print(e)
        return False

def get_bed(bed_id: int) -> dict:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()
        values = (bed_id)
        sql = ("""SELECT * FROM bed WHERE id = %s LIMIT 1""" % values)
        cursor.execute(sql)

        columns = [column[0] for column in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))

        return (data[0] if len(data) >= 1 else None)
    except Exception as e:
        print(e)
        return None

def get_beds_list(room_id: int) -> list:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()
        val = (room_id)
        sql = ("""SELECT * FROM bed WHERE room_id = %d""" % val)

        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        beds = []
        for row in cursor.fetchall():
            beds.append(dict(zip(columns, row)))
        
        return beds
    except Exception as e:
        print(e)
        return None