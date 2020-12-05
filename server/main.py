import os
import constants
import mysql.connector
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from flask import jsonify
from mysql.connector.errors import ProgrammingError
from models.data import data_blueprint
from models.room import room_blueprint
from models.emergency import emergency_blueprint

def load_settings() -> bool:
    env_path = join(dirname(__file__), ".env")
    success = os.path.isfile(env_path) and load_dotenv(env_path)
    if success:
        print("Settings loaded successfully")
    else:
        print("ERROR: Settings not loaded")
    return success



if not load_settings(): #Loads env variables, if not loaded the script ends
    exit()

app = Flask(__name__) #Server instance
app.register_blueprint(data_blueprint, url_prefix = constants.DATA_API_PREFIX)
app.register_blueprint(room_blueprint, url_prefix = constants.ROOM_API_PREFIX)
app.register_blueprint(emergency_blueprint, url_prefix = constants.EMERGENCY_API_PREFIX)

#Try to create a connection with DB
try:
    mydb = mysql.connector.connect(
        user = os.getenv("DATABASE_USER"),
        database = os.getenv("DATABASE_NAME"),
        password = os.getenv("DATABASE_PASSWORD")
    )
except ProgrammingError:
    #If the DB is not found, it is created
    mydb = mysql.connector.connect(
        user = os.getenv("DATABASE_USER"),
        password = os.getenv("DATABASE_PASSWORD")
    )

    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE pepperiot")
    cursor.execute("USE pepperiot")
    cursor.execute("CREATE TABLE room (id int auto_increment primary key, name_room varchar(50) NOT NULL UNIQUE)")
    cursor.execute("CREATE TABLE data_iot (id int auto_increment primary key, tmstp datetime NOT NULL, lux int, voc float, degree int, humidity int, room_id int, constraint fk_room foreign key (room_id) references room(id))")
    cursor.execute("CREATE TABLE emergency (id int auto_increment primary key, tmstp datetime NOT NULL, room_id int, data_id int, constraint fk_room_emergency foreign key (room_id) references room(id), constraint fk_data_emergency foreign key (data_id) references data_iot(id))")
    mydb.close()


@app.route("/") #Home page route
def home():
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = os.getenv("SERVER_PORT"), debug = os.getenv("DEBUG_MODE")) #Run server