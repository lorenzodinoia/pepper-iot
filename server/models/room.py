import os
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort
from mysql.connector.errors import IntegrityError

class Room:
    def __init__(self, id : int, name : str):
        self.id = id
        self.name = name

    def add_room(self, data):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()

            self.name = (data["name_room"])
            sql = ("""INSERT INTO room (name_room) VALUES ("%s")""" % self.name)
            cursor.execute(sql)
            mydb.commit()

            return 200
        except IntegrityError:
            return 400
        except Exception as e:
            print(e)
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()

    def get_rooms_list(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()

            cursor.execute("SELECT * FROM room ORDER BY id")
            room_columns = [column[0] for column in cursor.description]
            room_list = []
            for row in cursor.fetchall():
                room_list.append(dict(zip(room_columns, row)))

            rooms = []
            for room in room_list:
                room_id = room['id']
                room_name = room['name_room']
                new_room = {'id': room_id, 'name': room_name}
                rooms.append(new_room)

            return rooms
        except Exception:
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()
    
    def get_all_rooms(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM room INNER JOIN (SELECT bed.id AS bed_id, bed.inmate_id, inmate.name, inmate.surname, bed.room_id FROM bed INNER JOIN inmate ON bed.inmate_id = inmate.id) AS bed_inmate ON room.id = bed_inmate.room_id")
            room_columns = [column[0] for column in cursor.description]
            room_list = []
            for row in cursor.fetchall():
                room_list.append(dict(zip(room_columns, row)))

            #Create bed collection for each room
            rooms = []
            print(room_list)
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

            return rooms
        except:
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()


    def get_room(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                    user = os.getenv("DATABASE_USER"),
                    database = os.getenv("DATABASE_NAME"),
                    password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()
            val = (self.id)

            sql = ("""SELECT * FROM latest_env_data WHERE room_id = %d""" % val)
            cursor.execute(sql)
            env_data_columns = [column[0] for column in cursor.description]
            env_datas = []
            for row in cursor.fetchall():
                env_datas.append(dict(zip(env_data_columns, row)))

            sql = ("""SELECT bed.room_id, bed.id as bed_id, lvsi.* FROM bed INNER JOIN (SELECT last_vital_signs.id as last_vital_signs_id, last_vital_signs.tmstp AS lvs_tmstp, last_vital_signs.bpm, last_vital_signs.body_temperature, last_vital_signs.min_body_pressure, last_vital_signs.max_body_pressure, last_vital_signs.blood_oxygenation, last_vital_signs.inmate_id, inmate.name, inmate.surname, inmate.cf, inmate.date_birth FROM inmate INNER JOIN last_vital_signs ON inmate.id = last_vital_signs.inmate_id) AS lvsi ON bed.inmate_id = lvsi.inmate_id WHERE bed.room_id = %d""" % val)
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
            room = {'id' : self.id, 'name' : env_datas[0]['name_room'],'beds' : bed_results, 'env_data' : env_data}
                
            return room
        except Exception as e:
            print(e)
            return 500
        

room_blueprint = Blueprint('room', __name__)

@room_blueprint.route("/add", methods=["POST"]) #Add a new room
def add():
    if(request.json is not None):
        if("name_room" in request.json):
            obj = Room(None, None)
            value = obj.add_room(request.json)
            if(value == 200):
                return jsonify({"message" : "ok"})
            else:
                return abort(value)
        else:
            return abort(400)
    else:
        return abort(400)


@room_blueprint.route("/list", methods=["GET"]) #Get list of all avaible rooms
def get_list():
    obj = Room(None, None)
    value = obj.get_rooms_list()
    if(value != 500):
        return jsonify(value)
    else:
        return abort(value)

@room_blueprint.route("/all", methods=["GET"]) #Get list of all avaible rooms with beds and inmates
def get_all():
    obj = Room(None, None)
    value = obj.get_all_rooms()
    if(value != 500):
        return jsonify(value)
    else:
        return abort(value)

@room_blueprint.route("/", methods=["GET"]) #Get the single room with last env_data and all inmates
def get():
    room_id = request.args.get("id", default=None, type=int)
    if(room_id is not None):
        obj = Room(room_id, None)
        value = obj.get_room()
        if(value != 500):
            return jsonify(value)
        else:
            return abort(value)
    else:
        return abort(400)