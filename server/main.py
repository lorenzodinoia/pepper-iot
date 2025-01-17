import constants
import os
import mysql.connector
from os.path import join, dirname
from dotenv import load_dotenv
from mysql.connector.errors import ProgrammingError
from flask import Flask
from flask import jsonify
from flask_cors import CORS

from models.inmate import inmate_blueprint
from models.env_data import env_data_blueprint
from models.vital_data import vital_data_blueprint
from models.bed import bed_blueprint
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
app.register_blueprint(bed_blueprint, url_prefix = constants.BED_API_PREFIX)
app.register_blueprint(inmate_blueprint, url_prefix = constants.INMATE_API_PREFIX)
app.register_blueprint(env_data_blueprint, url_prefix = constants.ENV_DATA_API_PREFIX)
app.register_blueprint(vital_data_blueprint, url_prefix = constants.VITAL_DATA_API_PREFIX)
app.register_blueprint(room_blueprint, url_prefix = constants.ROOM_API_PREFIX)
app.register_blueprint(emergency_blueprint, url_prefix = constants.EMERGENCY_API_PREFIX)
CORS(app)

#Try to create a connection with DB
try:
    database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), database = os.getenv("DATABASE_NAME"), password = os.getenv("DATABASE_PASSWORD"))
except ProgrammingError:
    #If the DB is not found, it is created
    database = mysql.connector.connect(user = os.getenv("DATABASE_USER"), password = os.getenv("DATABASE_PASSWORD"))

    cursor = database.cursor()
    cursor.execute("CREATE DATABASE pepperiot")
    cursor.execute("USE pepperiot")
    cursor.execute("CREATE TABLE room (id int auto_increment primary key, name_room varchar(50) NOT NULL UNIQUE)")
    cursor.execute("CREATE TABLE inmate (id int auto_increment primary key, name varchar(50), surname varchar(50), cf varchar(16) UNIQUE, date_birth date)")
    cursor.execute("CREATE TABLE bed (id int auto_increment primary key, inmate_id int, room_id int, constraint fk_inmate foreign key (inmate_id) references inmate(id), constraint fk_room_bed foreign key (room_id) references room(id))")
    cursor.execute("CREATE TABLE environmental_data (id int auto_increment primary key, tmstp datetime NOT NULL, lux int, voc float, degree float, humidity int, room_id int, constraint fk_room foreign key (room_id) references room(id))")
    cursor.execute("CREATE TABLE vital_signs (id int auto_increment primary key, tmstp datetime NOT NULL, bpm int, body_temperature float, min_body_pressure int, max_body_pressure int, blood_oxygenation int, inmate_id int, constraint fk_inmate_data foreign key (inmate_id) references inmate(id))")
    cursor.execute("CREATE TABLE emergency (id INT AUTO_INCREMENT PRIMARY KEY, tmstp datetime NOT NULL, level_em INT, type_em INT, done BOOLEAN, env_data_id INT, vital_signs_id INT, bed_id INT, tags varchar(255) DEFAULT NULL,CONSTRAINT fk_env_emergency FOREIGN KEY (env_data_id) REFERENCES environmental_data(id), CONSTRAINT fk_vital_signs_emergency FOREIGN KEY (vital_signs_id) REFERENCES vital_signs(id), CONSTRAINT fk_bed_emergency FOREIGN KEY (bed_id) REFERENCES bed(id))")
    
    cursor.execute("CREATE VIEW last_vital_igns AS (SELECT vital_signs.id, tmstp, bpm, body_temperature, min_body_pressure, max_body_pressure, blood_oxygenation, vital_signs.inmate_id from vital_signs WHERE vital_signs.id IN (SELECT MAX(id) FROM vital_signs GROUP BY inmate_id))")
    cursor.execute("CREATE VIEW latest_env_data AS (SELECT environmental_data.id, tmstp, lux, voc, degree, humidity, room_id, name_room FROM room INNER JOIN environmental_data ON room.id = environmental_data.room_id WHERE environmental_data.id IN (SELECT MAX(id) FROM pepperiot.environmental_data GROUP BY room_id))")
database.close()


@app.route("/") #Home page route
def home():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = os.getenv("SERVER_PORT"), debug = os.getenv("DEBUG_MODE")) #Run server