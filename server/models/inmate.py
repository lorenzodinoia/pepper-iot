import os
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

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
    
    def get_inmate(self, id):
        self.id = id
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()

            val = (id)
            sql = ("""SELECT * FROM inmate WHERE id = %s""" % val)

            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))

            return data
        except Exception as e:
            print(e)
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()

inmate_blueprint = Blueprint('inmate', __name__)

@inmate_blueprint.route("/add", methods=["POST"]) #Add a new record
def add():
    data = request.json
    obj = Inmate(None, None, None, None, None)
    value = obj.add_inmate(data)
    if(value == 200):
        return jsonify({"message" : "ok"})
    else:
        return abort(value)

@inmate_blueprint.route("/get", methods=["GET"]) #Get inmate from id
def get():
    inmate_id = request.args.get('id', default=None, type=int) #Use /inmate?id=... for URL parameter passing
    if(inmate_id is not None):
        obj = Inmate(None, None, None, None, None)
        value = obj.get_inmate(inmate_id)
        if(value != 500):
            return jsonify(value)
        else:
            return abort(value)
    else:
        return abort(400)