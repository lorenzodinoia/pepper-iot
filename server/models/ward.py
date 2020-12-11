import os
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

class Ward:
    def __init__(self, id : int, name : str):
        self.id = id
        self.name = name
    
    def get_ward_list(self):
        mydb = None
        try:
            mydb = mysql.connector.connect(
                user = os.getenv("DATABASE_USER"),
                database = os.getenv("DATABASE_NAME"),
                password = os.getenv("DATABASE_PASSWORD")
            )
            cursor = mydb.cursor()

            cursor.execute("SELECT * FROM ward")
            ward_columns = [column[0] for column in cursor.description]
            ward_list = []
            for row in cursor.fetchall():
                ward_list.append(dict(zip(ward_columns, row)))

            return ward_list
        except Exception:
            return 500
        finally:
            if(mydb.is_connected()):
                mydb.close()


ward_blueprint = Blueprint('ward', __name__)

@ward_blueprint.route("/all", methods=["GET"]) #Get list of all avaible rooms
def get_all():
    obj = Ward(None, None)
    value = obj.get_ward_list()
    if(value != 500):
        return jsonify(value)
    else:
        return abort(value)