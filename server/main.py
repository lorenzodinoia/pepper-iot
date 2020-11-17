import mysql.connector
from flask import Flask
from flask import jsonify
from mysql.connector.errors import DatabaseError, ProgrammingError
from models.data import data_blueprint
from models.room import room_blueprint

#Prefix for API
DATA_API_PREFIX = "/data"
ROOM_API_PREFIX = "/room"

#Constants for DB connection
USER_DB = "root"
DATABASE = "pepperiot"
PASSWORD = "password"

app = Flask(__name__) #Server instance

app.register_blueprint(data_blueprint, url_prefix=DATA_API_PREFIX)
app.register_blueprint(room_blueprint, url_prefix=ROOM_API_PREFIX)

#Try to create a connection with DB
try:
    mydb = mysql.connector.connect(
        user=USER_DB,
        database=DATABASE,
        password=PASSWORD
    )
except ProgrammingError:
    #If the DB is not found, it is created
    mydb = mysql.connector.connect(
        user=USER_DB,
        password=PASSWORD
    )

    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE pepperiot")
    cursor.execute("USE pepperiot")
    cursor.execute("CREATE TABLE room (id int auto_increment primary key, name_room varchar(50))")
    cursor.execute("CREATE TABLE data_iot (id int auto_increment primary key, tmspt datetime, lux int, vox int, degree int, humidity int, room_id int, constraint fk_room foreign key (room_id) references room(id))")

    mydb.close()


@app.route("/") #Home page route
def home():
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) #Run server
