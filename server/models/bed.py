import os
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

class Bed:
    def __init__(self, id : int, inmate_id : int, room_id : int):
        self.id = id
        self.inmate_id = inmate_id
        self.room_id = room_id
    
    def add_bed(self, data):
        if(data is not None):
            self.inmate_id = None
            self.room_id = None
            if("inmate_id" in data):
                self.inmate_id = data["inmate_id"]
            else:
                return 400
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

                val = (self.inmate_id, self.room_id)
                sql = ("""INSERT INTO bed (inmate_id, room_id) VALUES (%d, %d)""" % val)
                
                cursor.execute(sql)
                mydb.commit()

                return 200
            except:
                return 500
            finally:
                if(mydb.is_connected()):
                    mydb.close()
        else:
            return 400
    
    def get_bed(self, id):
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
            sql = ("""SELECT * FROM bed WHERE id = %s""" % val)

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

    def get_bed_list(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()
            val = (self.room_id)
            sql = ("""SELECT * FROM bed WHERE id = %d""" % val)

            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            beds = []
            for row in cursor.fetchall():
                beds.append(dict(zip(columns, row)))
            
            return beds
        except Exception as e:
            print(e)
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()



bed_blueprint = Blueprint('bed', __name__)

@bed_blueprint.route("/add", methods=["POST"]) #Add a new bed
def add():
    data = request.json
    if(data is not None):
        obj = Bed(None, None, None)
        value = obj.add_bed(data)
        if(value == 200):
            return jsonify({"message" : "ok"})
        else:
            return abort(value)
    else:
        return abort(400)

@bed_blueprint.route("/", methods=["GET"]) #Get bed from id
def get():
    bed_id = request.args.get("id", default=None, type=int)
    if(bed_id is not None):
        obj = Bed(None, None, None)
        value = obj.get_bed(bed_id)
        if(value != 500):
            return jsonify(value)
        else:
            return abort(value)
    else:
        return abort(400)

@bed_blueprint.route("/all", methods=["GET"]) #Get the list of all beds in a room
def get_all():
    room_id = request.args.get("room_id", default=None, type=int)
    if(room_id is not None):
        obj = Bed(None, None, room_id)
        value = obj.get_bed_list()
        if(value != 500):
            return jsonify(value)
        else:
            return abort(value)
    else:
        return abort(400)