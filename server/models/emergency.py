import os
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort
from datetime import datetime
import mysql.connector

"""
Attribute description:
level_em is an index of the priority of the emergency in a scale between 0 and 2
type_em indicates the type of emergency. It could be of three different types:
    0 - env_data emergency
    1 - vital_data emergency
    2 - emergency button (AWS)
done indicates if the emergency is already managed or not
"""
class Emergency:
    def __init__(self, id : int, tmstp : str, level_em : int, type_em : int, done : bool, env_data_id : int, vital_signs_id : int, bed_id : int):
        self.id = id
        self.tmstp = tmstp
        self.level_em = level_em
        self.type_em = type_em
        self.done = done
        self.env_data_id = env_data_id
        self.vital_signs_id = vital_signs_id
        self.bed_id = bed_id

    def add_emergency(self, data):

        sql = None

        if(data is not None):
            if("level_em" in data):
                self.level_em = data["level_em"]
            else:
                return 400
            if("type_em" in data):
                self.type_em = data["type_em"]
            else:
                return 400
            
            #Check if the emergency is already in the db in the vital_signs emergency form
            mydb = None
            try:
                mydb = mysql.connector.connect(
                    user = os.getenv("DATABASE_USER"),
                    database = os.getenv("DATABASE_NAME"),
                    password = os.getenv("DATABASE_PASSWORD")
                )

                cursor = mydb.cursor()

                if(self.type_em == 0):
                    if("env_data_id" in data):
                        self.env_data_id = data["env_data_id"]
                        val = (self.level_em, self.type_em, self.env_data_id)
                        sql = ("""INSERT INTO emergency (tmstp, level_em, type_em, done, env_data_id) VALUES (NOW(), %d, %d, False, %d)""" % val)
                        cursor.execute(sql)
                        mydb.commit()
                    else: 
                        return 400
                elif (self.type_em == 1):
                    if("vital_signs_id" in data):
                        self.vital_signs_id = data["vital_signs_id"]
                        val = (self.level_em, self.type_em, self.vital_signs_id)
                        sql = ("""INSERT INTO emergency (tmstp, level_em, type_em, done, vital_signs_id) VALUES (NOW(), %d, %d, False, %d)""" % val)
                        cursor.execute(sql)
                        mydb.commit()
                    else:
                        return 400

                elif(self.type_em == 2):
                    if("bed_id" in data):
                        self.bed_id = data["bed_id"]

                        #Read the bed
                        val = self.bed_id
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
                            if(difference.seconds < 60) : 
                                valid = False

                        if(valid):
                            val = (self.level_em, self.type_em, self.bed_id)
                            sql = ("""INSERT INTO emergency (tmstp, level_em, type_em, done, bed_id) VALUES (NOW(), %d, %d, False, %d)""" % val)
                            cursor.execute(sql)
                            mydb.commit()
                    else:
                        return 400    
                else:
                    return 400

                return 200
            except Exception as e:
                print(e)
                return 500
            finally:
                if(mydb.is_connected()):
                    mydb.close()
            
        else:
            return abort(400)

    def get_emergency_list(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()
            sql = """SELECT * FROM pepperiot.emergency WHERE done = False"""
            cursor.execute(sql)

            emergency_columns = [column[0] for column in cursor.description]
            emergency_list = []
            for row in cursor.fetchall():
                emergency_list.append(dict(zip(emergency_columns, row)))

            queue = []
            env_data_em = []
            vital_signs_em = []
            button_em = []
            for emergency in emergency_list:
                if(emergency["type_em"] == 0):
                    new_emergency = {"id" : emergency["id"], "tmstp" : emergency["tmstp"], "level_em" : emergency["level_em"], "type_em" : emergency["type_em"], "env_data_id" : emergency["env_data_id"]}
                    env_data_em.append(new_emergency)
                elif(emergency["type_em"] == 1):
                    new_emergency = {"id" : emergency["id"], "tmstp" : emergency["tmstp"], "level_em" : emergency["level_em"], "type_em" : emergency["type_em"], "vital_signs_id" : emergency["vital_signs_id"]}
                    vital_signs_em.append(new_emergency)
                else:
                    new_emergency = {"id" : emergency["id"], "tmstp" : emergency["tmstp"], "level_em" : emergency["level_em"], "type_em" : emergency["type_em"], "bed_id" : emergency["bed_id"]}
                    button_em.append(new_emergency)

            for vital_sign in vital_signs_em:
                queue.append(vital_sign)
            for button in button_em:
                queue.append(button)
            for env in env_data_em:
                queue.append(env)

            

            return queue
        except Exception as e:
            print(e)
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()

    def set_em_done(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()

            val = (self.id)
            sql = ("""UPDATE emergency SET done = TRUE WHERE id = %d""" % val)
            print(sql)
            cursor.execute(sql)
            mydb.commit()

            return 200
        except Exception as e:
            print(e)
            return 500
        finally:
            if mydb.is_connected():
                mydb.close()

    def get_next(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()
            sql = """SELECT * FROM pepperiot.emergency WHERE done = 0 ORDER BY tmstp ASC LIMIT 1;""" #Get latest emergency
            cursor.execute(sql)

            emergency_columns = [column[0] for column in cursor.description]
            emergency_list = []
            for row in cursor.fetchall():
                emergency_list.append(dict(zip(emergency_columns, row)))

            emergency_id = emergency_list[0]["id"]
            emergency_type = emergency_list[0]["type_em"]
            emergency = {"id": emergency_id, "type": emergency_type, "level": emergency_list[0]["level_em"], "tmstp": emergency_list[0]["tmstp"]}

            if emergency_type == 0: #Environmental emergency
                sql = ("""SELECT environmental_data.*, room.* FROM emergency INNER JOIN environmental_data ON environmental_data.id = emergency.env_data_id INNER JOIN room ON room.id = environmental_data.room_id WHERE emergency.id = %d LIMIT 1;""" % (emergency_id))
                cursor.execute(sql)
                
                join_columns = [column[0] for column in cursor.description]
                join_list = []
                for row in cursor.fetchall():
                    join_list.append(dict(zip(join_columns, row)))

                emergency_room_name = join_list[0]["name_room"]
                env_data = {"lux": join_list[0]["lux"], "voc": join_list[0]["voc"], "temperature": join_list[0]["degree"], "humidity": join_list[0]["humidity"]}
                emergency["env_data"] = env_data
                emergency["room_name"] = emergency_room_name
                return emergency
            if emergency_type == 1: #Vital emergency
                sql = ("""SELECT emergency.bed_id, vital_signs.* FROM emergency INNER JOIN vital_signs ON vital_signs.id = emergency.vital_signs_id WHERE emergency.id = %d LIMIT 1;""" % (emergency_id))
                cursor.execute(sql)
                
                join_columns = [column[0] for column in cursor.description]
                join_list = []
                for row in cursor.fetchall():
                    join_list.append(dict(zip(join_columns, row)))
                
                emergency_room_name = emergency_list[0]["bed_id"]
                env_data = {"bpm": join_list[0]["bpm"], "body_temperature": join_list[0]["body_temperature"], "min_body_pressure": join_list[0]["min_body_pressure"], 
                            "max_body_pressure": join_list[0]["max_body_pressure"], "blood_oxygenation": join_list[0]["blood_oxygenation"]}
                emergency["vital_signs"] = env_data
                emergency["bed_id"] = emergency_room_name
                return emergency
            if emergency_type == 2: #Button pressed
                pass
        except Exception as e:
            print(e)
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()


emergency_blueprint = Blueprint('emergency', __name__)

@emergency_blueprint.route("/add", methods=["POST"]) #Add a new emergency
def add():
    data = request.json
    emergency = Emergency(None, None, None, None, None, None, None, None)
    value = emergency.add_emergency(data)
    if(value == 200):
        return jsonify(value)
    else:
        return abort(value)

@emergency_blueprint.route("/", methods=["GET"]) #Get a list of active emergencies
def get():
    emergency = Emergency(None, None, None, None, None, None, None, None)
    value = emergency.get_emergency_list()
    if(value != 500):
        return jsonify(value)
    else:
        return abort(value)

@emergency_blueprint.route("/done", methods=["POST"]) #Set an emergency as done
def set_done():
    emergency_id = request.args.get("id", default=None, type=int)
    if(emergency_id is not None):
        emergency = Emergency(emergency_id, None, None, None, None, None, None, None)
        value = emergency.set_em_done()
        if(value == 200):
            return jsonify(value)
        else:
            return abort(value)
    else:
        return abort(400)

@emergency_blueprint.route("/next", methods=["GET"]) #Get latest emergency
def get_latest():
    emergency = Emergency(None, None, None, None, None, None, None, None)
    value = emergency.get_next()
    if(value != 500):
        return jsonify(value)
    else:
        return abort(value)