import os
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

room_blueprint = Blueprint('room', __name__)

@room_blueprint.route("/add", methods=["POST"]) #Add a new room
def add():
    data = request.json
    if ((data is not None) and ("name" in data)):
        if (add_room(data["name"])):
            return jsonify({"message": "OK"})
        else:
            return abort(500)
    else:
        return abort(400)

@room_blueprint.route("/list", methods=["GET"]) #Get list of all avaible rooms
def get_list():
    result = get_rooms_list()
    if (result is not None):
        return jsonify(result)
    else:
        return abort(500)

@room_blueprint.route("/all", methods=["GET"]) #Get list of all avaible rooms with beds and inmates
def get_all():
    value = get_all_rooms()
    if(value is not None):
        return jsonify(value)
    else:
        return abort(500)

@room_blueprint.route("/", methods=["GET"]) #Get the single room with last env_data and all inmates
def get():
    room_id = request.args.get("id", default=None, type=int)
    if (room_id is not None):
        room = get_room(room_id)
        if (room is not None):
            return jsonify(room)
        else:
            return abort(500)
    else:
        return abort(400)


def sortById(e):
    return e["id"]

def add_room(room_name: str) -> bool:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()
        sql = ("""INSERT INTO room (name_room) VALUES ("%s")""" % (room_name))
        cursor.execute(sql)
        database.commit()
        return True
    except Exception as e:
        print(e)
        return False

def get_rooms_list() -> list:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()
        cursor.execute("SELECT * FROM room ORDER BY id")

        room_columns = [column[0] for column in cursor.description]
        rooms = []
        for row in cursor.fetchall():
            room = dict(zip(room_columns, row))
            room_id = room['id']
            room_name = room['name_room']
            new_room = {'id': room_id, 'name': room_name}
            rooms.append(new_room)

        return rooms
    except Exception as e:
        print(e)
        return None

def get_room(room_id: int) -> dict:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()
        values = (room_id)

        sql = ("""SELECT * FROM latest_env_data WHERE room_id = %d""" % values)
        cursor.execute(sql)
        env_data_columns = [column[0] for column in cursor.description]
        env_datas = []
        for row in cursor.fetchall():
            env_datas.append(dict(zip(env_data_columns, row)))

        sql = ("""SELECT bed.room_id, bed.id as bed_id, lvsi.* FROM bed INNER JOIN (SELECT last_vital_signs.id as last_vital_signs_id, last_vital_signs.tmstp AS lvs_tmstp, last_vital_signs.bpm, last_vital_signs.body_temperature, last_vital_signs.min_body_pressure, last_vital_signs.max_body_pressure, last_vital_signs.blood_oxygenation, last_vital_signs.inmate_id, inmate.name, inmate.surname, inmate.cf, inmate.date_birth FROM inmate INNER JOIN last_vital_signs ON inmate.id = last_vital_signs.inmate_id) AS lvsi ON bed.inmate_id = lvsi.inmate_id WHERE bed.room_id = %d""" % values)
        cursor.execute(sql)
        room_columns = [column[0] for column in cursor.description]
        bed_list = []
        for row in cursor.fetchall():
            bed_list.append(dict(zip(room_columns, row)))

        bed_results = []
        for bed_element in bed_list:
            vital_signs = {'id' : bed_element['last_vital_signs_id'], 'tmstp' : bed_element['lvs_tmstp'], 'bpm' : bed_element['bpm'], 'body_temperature' : bed_element['body_temperature'], 'min_body_pressure' : bed_element['min_body_pressure'], 'max_body_pressure' : bed_element['max_body_pressure'], 'blood_oxygenation' : bed_element['blood_oxygenation']}
            inmate = {'id': bed_element['inmate_id'], 'name': bed_element['name'], 'surname': bed_element['surname'], 'cf' : bed_element['cf'], 'date_birth' : bed_element['date_birth'], 'vital_signs' : vital_signs}
            bed = {'id': bed_element['bed_id'], 'inmate': inmate}
            bed_results.append(bed)

        env_data = {'id' : env_datas[0]['id'], 'tmstp' : env_datas[0]['tmstp'], 'lux' : env_datas[0]['lux'], 'voc' : env_datas[0]['voc'], 'degree' : env_datas[0]['degree'], 'humidity' : env_datas[0]['humidity']}
        room = {'id' : room_id, 'name' : env_datas[0]['name_room'],'beds' : bed_results, 'env_data' : env_data}
            
        return room
    except Exception as e:
        print(e)
        return None

def get_all_rooms() -> dict:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()
        cursor.execute("SELECT * FROM room INNER JOIN (SELECT bed.id AS bed_id, bed.inmate_id, inmate.name, inmate.surname, bed.room_id FROM bed INNER JOIN inmate ON bed.inmate_id = inmate.id) AS bed_inmate ON room.id = bed_inmate.room_id ORDER BY id ASC")
        room_columns = [column[0] for column in cursor.description]
        room_list = []
        for row in cursor.fetchall():
            room_list.append(dict(zip(room_columns, row)))

        #Create bed collection for each room
        rooms = []
        for room in room_list:
            inmate = {'id': room['inmate_id'], 'name': room['name'], 'surname': room['surname']}
            bed = {'id': room['bed_id'], 'inmate': inmate}
            founded_rooms = list(filter(lambda element: element.get('id') == room['id'], rooms))
            if len(founded_rooms) == 0: #Room doesn't exists
                room_id = room['id']
                room_name = room['name_room']
                room_beds = []
                room_beds.append(bed)
                new_room = {'id': room_id, 'name': room_name, 'beds': room_beds}
                rooms.append(new_room)
            else:
                existing_room = founded_rooms[0]
                existing_room['beds'].append(bed)

        for room in rooms:
            room["beds"].sort(key=sortById)

        return rooms
    except Exception as e:
        print(e)
        return None