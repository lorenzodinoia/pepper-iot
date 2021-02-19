import os
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort
from datetime import datetime
import mysql.connector

"""
Attributes description:
level_em is an index of the priority of the emergency in a scale between 0 and 2
type_em indicates the type of emergency. It could be of three different types:
    0 - env_data emergency
    1 - vital_data emergency
    2 - emergency button (AWS)
    3 - send pepper (dashboard)
done indicates if the emergency is already managed or not
"""

emergency_blueprint = Blueprint('emergency', __name__)

@emergency_blueprint.route("/add", methods=["POST"]) #Add a new emergency
def add():
    data = request.json
    if (("level_em" in data) and ("type_em" in data) and ("tags" in data)):
        level = data["level_em"]
        emergency_type = data["type_em"]
        tags = data["tags"]
        env_data_id = (data["env_data_id"] if ("env_data_id" in data) else None)
        vital_signs_id = (data["vital_signs_id"] if ("vital_signs_id" in data) else None)
        bed_id = (data["bed_id"] if ("bed_id" in data) else None)

        if (add_emergency(level, emergency_type, tags, env_data_id, vital_signs_id, bed_id)):
            return jsonify({"Message": "OK"})
        else:
            return abort(500)
    else:
        return abort(400)

@emergency_blueprint.route("/", methods=["GET"]) #Get a list of active emergencies
def get():
    result = get_emergency_list()
    if (result is not None):
        return jsonify(result)
    else:
        return abort(500)

@emergency_blueprint.route("/done", methods=["POST"]) #Set an emergency as done
def set_done():
    emergency_id = request.args.get("id", default=None, type=int)
    if(emergency_id is not None):
        value = set_done(emergency_id)
        if (value):
            return jsonify({"message": "Ok"})
        else:
            return abort(500)
    else:
        return abort(400)

@emergency_blueprint.route("/next", methods=["GET"]) #Get latest emergency
def get_next():
    value = get_next()
    if(value is not None):
        return jsonify(value)
    else:
        return abort(500)



def add_emergency(level: int, emergency_type: int, tags: str, env_data_id: int, vital_signs_id: int, bed_id: int) -> bool:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()

        if ((emergency_type == 0) and (env_data_id is not None)):
            val = (level, emergency_type, env_data_id, tags)
            sql = ("""INSERT INTO emergency (tmstp, level_em, type_em, done, env_data_id, tags) VALUES (NOW(), %d, %d, False, %d, "%s")""" % val)
            cursor.execute(sql)
            database.commit()
        elif ((emergency_type == 1) and (vital_signs_id is not None) and (bed_id is not None)):
            val = (level, emergency_type, vital_signs_id, bed_id, tags)
            sql = ("""INSERT INTO emergency (tmstp, level_em, type_em, done, vital_signs_id, bed_id, tags) VALUES (NOW(), %d, %d, False, %d, %d, "%s")""" % val)
            cursor.execute(sql)
            database.commit()
        elif (((emergency_type == 2) or (emergency_type == 3)) and (bed_id is not None)):
            #Read the bed
            val = (bed_id)
            sql = ("""SELECT * FROM bed WHERE id = %d""" % val)
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            join = []
            for row in cursor.fetchall():
                join.append(dict(zip(columns, row)))

            #Get the list of emergencies not handeld that refers to the inmate of bed get previously
            val = join[0]["inmate_id"]
            sql = ("""SELECT vital_signs.*, emergency.id, emergency.tmstp AS tmstp_em, emergency.level_em, emergency.type_em, emergency.done FROM emergency INNER JOIN vital_signs ON emergency.vital_signs_id = vital_signs.id WHERE inmate_id = %d AND done = False""" % val)
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            list = []
            for row in cursor.fetchall():
                list.append(dict(zip(columns, row)))
            
            #Check if there is another emergency for the same inmate that has a timestamp difference below 1 min.
            valid = True
            now = datetime.now()
            for vital_sign in list:
                difference = now - vital_sign["tmstp_em"]
                if (difference.seconds < 60) : 
                    valid = False

            if (valid):
                val = (level, emergency_type, bed_id)
                sql = ("""INSERT INTO emergency (tmstp, level_em, type_em, done, bed_id) VALUES (NOW(), %d, %d, False, %d)""" % val)
                cursor.execute(sql)
                database.commit()
        else:
            raise Exception

        if database.is_connected():
            database.close()
        return True
    except Exception as e:
        if database.is_connected():
            database.close()
        return False


def set_done(id : int) -> bool:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()

        val = (id)
        sql = ("""UPDATE emergency SET done = TRUE WHERE id = %d""" % val)
        cursor.execute(sql)
        database.commit()

        if database.is_connected():
            database.close()
        return True
    except Exception as e:
        print(e)
        if database.is_connected():
            database.close()
        return False


def get_next() -> dict:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()
        sql = """SELECT * FROM pepperiot.emergency WHERE done = 0 ORDER BY tmstp ASC LIMIT 1;""" #Get latest emergency
        cursor.execute(sql)

        emergency_columns = [column[0] for column in cursor.description]
        emergency_list = []
        for row in cursor.fetchall():
            emergency_list.append(dict(zip(emergency_columns, row)))

        if len(emergency_list) == 0:
            if(database.is_connected()):
                database.close()
            return {}

        emergency_id = emergency_list[0]["id"]
        emergency_type = emergency_list[0]["type_em"]
        emergency = {"id": emergency_id, "type": emergency_type, "level": emergency_list[0]["level_em"], "tags": emergency_list[0]["tags"], "tmstp": emergency_list[0]["tmstp"]}

        if emergency_type == 0: #Environmental emergency
            sql = ("""SELECT environmental_data.*, room.id AS room_id, room.name_room AS room_name FROM emergency INNER JOIN environmental_data ON environmental_data.id = emergency.env_data_id INNER JOIN room ON room.id = environmental_data.room_id WHERE emergency.id = %d LIMIT 1;""" % (emergency_id))
            cursor.execute(sql)
            
            join_columns = [column[0] for column in cursor.description]
            join_list = []
            for row in cursor.fetchall():
                join_list.append(dict(zip(join_columns, row)))

            room = {"id": join_list[0]["room_id"], "name": join_list[0]["room_name"]}
            env_data = {"lux": join_list[0]["lux"], "voc": join_list[0]["voc"], "temperature": join_list[0]["degree"], "humidity": join_list[0]["humidity"]}
            emergency["env_data"] = env_data
            emergency["room"] = room
            
        elif emergency_type == 1: #Vital emergency
            sql = ("""SELECT emergency.bed_id, vital_signs.* FROM emergency INNER JOIN vital_signs ON vital_signs.id = emergency.vital_signs_id WHERE emergency.id = %d LIMIT 1;""" % (emergency_id))
            cursor.execute(sql)
            
            join_columns = [column[0] for column in cursor.description]
            join_list = []
            for row in cursor.fetchall():
                join_list.append(dict(zip(join_columns, row)))
            
            emergency_bed_id = emergency_list[0]["bed_id"]
            env_data = {"bpm": join_list[0]["bpm"], "body_temperature": join_list[0]["body_temperature"], "min_body_pressure": join_list[0]["min_body_pressure"], 
                        "max_body_pressure": join_list[0]["max_body_pressure"], "blood_oxygenation": join_list[0]["blood_oxygenation"]}
            emergency["vital_signs"] = env_data
            emergency["bed_id"] = emergency_bed_id
        
        elif ((emergency_type == 2) or (emergency_type == 3)): #Button pressed or send pepper from dashboard
            emergency_bed_id = emergency_list[0]["bed_id"]
            emergency["bed_id"] = emergency_bed_id

        if(database.is_connected()):
            database.close()
        return emergency
    except Exception as e:
        print(e)
        if(database.is_connected()):
            database.close()
        return None


def get_emergency_list() -> list:
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()

        sql = """SELECT * FROM pepperiot.emergency WHERE done = False"""
        cursor.execute(sql)

        emergency_columns = [column[0] for column in cursor.description]
        emergency_list = []
        for row in cursor.fetchall():
            emergency = dict(zip(emergency_columns, row))
            new_emergency = {}

            emergency_id = emergency["id"]
            emergency_type = emergency["type_em"]
            new_emergency = {"id": emergency_id, "type": emergency_type, "level": emergency["level_em"], "tags": emergency["tags"], "tmstp": emergency["tmstp"]}

            if emergency_type == 0: #Environmental emergency
                sql = ("""SELECT environmental_data.*, room.id AS room_id, room.name_room AS room_name FROM emergency INNER JOIN environmental_data ON environmental_data.id = emergency.env_data_id INNER JOIN room ON room.id = environmental_data.room_id WHERE emergency.id = %d LIMIT 1;""" % (emergency_id))
                cursor.execute(sql)
                
                join_columns = [column[0] for column in cursor.description]
                join_list = []
                for row in cursor.fetchall():
                    join_list.append(dict(zip(join_columns, row)))

                room = {"id": join_list[0]["room_id"], "name": join_list[0]["room_name"]}
                env_data = {"lux": join_list[0]["lux"], "voc": join_list[0]["voc"], "temperature": join_list[0]["degree"], "humidity": join_list[0]["humidity"]}
                new_emergency["env_data"] = env_data
                new_emergency["room"] = room
            if emergency_type == 1: #Vital emergency
                sql = ("""SELECT emergency.bed_id, vital_signs.* FROM emergency INNER JOIN vital_signs ON vital_signs.id = emergency.vital_signs_id WHERE emergency.id = %d LIMIT 1;""" % (emergency_id))
                cursor.execute(sql)
                
                join_columns = [column[0] for column in cursor.description]
                join_list = []
                for row in cursor.fetchall():
                    join_list.append(dict(zip(join_columns, row)))
                
                emergency_bed_id = emergency["bed_id"]
                env_data = {"bpm": join_list[0]["bpm"], "body_temperature": join_list[0]["body_temperature"], "min_body_pressure": join_list[0]["min_body_pressure"], 
                            "max_body_pressure": join_list[0]["max_body_pressure"], "blood_oxygenation": join_list[0]["blood_oxygenation"]}
                new_emergency["vital_signs"] = env_data
                new_emergency["bed_id"] = emergency_bed_id
            if ((emergency_type == 2) or (emergency_type == 3)): #Button pressed
                emergency_bed_id = emergency["bed_id"]
                new_emergency["bed_id"] = emergency_bed_id

            emergency_list.append(new_emergency)

        if database.is_connected():
            database.close()
        return emergency_list
    except Exception as e:
        print(e)
        if database.is_connected():
            database.close()
        return None