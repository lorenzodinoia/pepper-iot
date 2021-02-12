import os
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

from models.emergency import Emergency

class Inmate:
    def __init__(self, id : int, name : str, surname : str, cf : str, date_birth : str):
        self.id = id
        self.name = name
        self.surname = surname
        self.cf = cf
        self.date_birth = date_birth

    def add_inmate(self, data):
        if(data is not None):
            self.name = None
            self.surname = None
            self.cf = None
            self.date_birth = None
            if("name" in data):
                self.name = data["name"]
            else:
                return 400
            if("surname" in data):
                self.surname = data["surname"]
            else:
                return 400
            if("cf" in data):
                self.cf = data["cf"]
            else:
                return 400
            if("date_birth" in data):
                self.date_birth = data["date_birth"]
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

                val = (self.name, self.surname, self.cf, self.date_birth)
                sql = ("""INSERT INTO inmate (name, surname, cf, date_birth) VALUES ('%s', '%s', '%s', '%s')""" % val)
                
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
            return  400
    
    def get_inmate(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()

            val = (self.id)
            sql = ("""SELECT inmate.*, last_vital_signs.id AS lvs_id, last_vital_signs.tmstp, last_vital_signs.bpm, last_vital_signs.body_temperature, last_vital_signs.min_body_pressure, last_vital_signs.max_body_pressure, last_vital_signs.blood_oxygenation FROM inmate INNER JOIN last_vital_signs ON inmate.id = last_vital_signs.inmate_id WHERE inmate.id = %s""" % val)

            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))

            print(data)
            inmate_data = data[0]
            vital_signs = {'id' : inmate_data['lvs_id'], 'tmstp' : inmate_data['tmstp'], 'bpm' : inmate_data['bpm'], 'body_temperature' : inmate_data['body_temperature'], 'min_body_pressure' : inmate_data['min_body_pressure'], 'max_body_pressure' : inmate_data['max_body_pressure'], 'blood_oxygenation' : inmate_data['blood_oxygenation']}
            new_inmate = {'id' : inmate_data['id'], 'name' : inmate_data['name'], 'surname' : inmate_data['surname'], 'cf' : inmate_data['cf'], 'date_birth' : inmate_data['date_birth'], 'vital_signs' : vital_signs}

            return new_inmate
        except Exception as e:
            print(e)
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()

    def send_pepper(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()

            val = (self.id)
            sql = ("""SELECT id FROM pepperiot.bed WHERE inmate_id = %d LIMIT 1;""" % val)

            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))

            bed_id = data[0]["id"]
            emergency_obj = Emergency(None, None, None, None, None, None, None, None, None)
            data = {"level_em" : 0, "type_em" : 3, "bed_id" : bed_id, "tags": ""}
            value = emergency_obj.add_emergency(data)
            if(value != 200):
                return 500

            return 200
        except:
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()


inmate_blueprint = Blueprint('inmate', __name__)

@inmate_blueprint.route("/add", methods=["POST"]) #Add a new record
def add():
    data = request.json
    value = add_inmate(data)
    if(value == 200):
        return jsonify({"message" : "ok"})
    else:
        return abort(value)

@inmate_blueprint.route("/", methods=["GET"]) #Get inmate from id
def get():
    inmate_id = request.args.get('id', default=None, type=int) #Use /inmate?id=... for URL parameter passing
    if(inmate_id is not None):
        value = get_inmate(inmate_id)
        if(value is not None):
            return jsonify(value)
        else:
            return abort(500)
    else:
        return abort(400)

@inmate_blueprint.route("/sendPepper", methods=["POST"]) #Create an emergency with type_em = 3
def set_done():
    inmate_id = request.args.get("id", default=None, type=int)
    if(inmate_id is not None):
        value = send_pepper(inmate_id)
        if (value == 200):
            return jsonify({"message": "Ok"})
        else:
            return abort(value)
    else:
        return abort(400)

def add_inmate(self, data):
    if(data is not None):
        name = None
        surname = None
        cf = None
        date_birth = None
        if(("name" in data) and ("surname" in data) and ("cf" in data) and ("date_birth" in data)):
            name = data["name"]
            surname = data["surname"]
            cf = data["cf"]
            date_birth = data["date_birth"]
        else:
            return 400
        
        try:
            database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
            cursor = database.cursor()

            val = (name, surname, cf, date_birth)
            sql = ("""INSERT INTO inmate (name, surname, cf, date_birth) VALUES ('%s', '%s', '%s', '%s')""" % val)
            
            cursor.execute(sql)
            database.commit()
            if(database.is_connected()):
                database.close()
            return 200
        except Exception as e:
            print(e)
            if(database.is_connected()):
                database.close()
            return 500    
    else:
        return  400

def get_inmate(id : int):
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()

        val = (id)
        sql = ("""SELECT inmate.*, last_vital_signs.id AS lvs_id, last_vital_signs.tmstp, last_vital_signs.bpm, last_vital_signs.body_temperature, last_vital_signs.min_body_pressure, last_vital_signs.max_body_pressure, last_vital_signs.blood_oxygenation FROM inmate INNER JOIN last_vital_signs ON inmate.id = last_vital_signs.inmate_id WHERE inmate.id = %s""" % val)

        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))

        if(data is not None):
            inmate_data = data[0]
            vital_signs = {'id' : inmate_data['lvs_id'], 'tmstp' : inmate_data['tmstp'], 'bpm' : inmate_data['bpm'], 'body_temperature' : inmate_data['body_temperature'], 'min_body_pressure' : inmate_data['min_body_pressure'], 'max_body_pressure' : inmate_data['max_body_pressure'], 'blood_oxygenation' : inmate_data['blood_oxygenation']}
            new_inmate = {'id' : inmate_data['id'], 'name' : inmate_data['name'], 'surname' : inmate_data['surname'], 'cf' : inmate_data['cf'], 'date_birth' : inmate_data['date_birth'], 'vital_signs' : vital_signs}
        else:
            new_inmate = []

        if(database.is_connected()):
            database.close()
        return new_inmate
    except Exception as e:
        print(e)
        if(database.is_connected()):
            database.close()
        return None

#TODO rimuovere chiamata emergenza come classe
def send_pepper(id : int):
    try:
        database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
        cursor = database.cursor()

        val = (id)
        sql = ("""SELECT id FROM pepperiot.bed WHERE inmate_id = %d LIMIT 1;""" % val)

        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))

        if(data is not None):
            bed_id = data[0]["id"]
            emergency_obj = Emergency(None, None, None, None, None, None, None, None, None)
            data = {"level_em" : 0, "type_em" : 3, "bed_id" : bed_id, "tags": ""}
            value = emergency_obj.add_emergency(data)
            if(value != 200):
                if(database.is_connected()):
                    database.close()
                return 500
            if(database.is_connected()):
                database.close()
            return 200
        else:
            if(database.is_connected()):
                database.close()
            return 400
    except Exception as e:
        print(e)
        if(database.is_connected()):
            database.close()
        return 500