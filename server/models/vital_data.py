import os
import constants
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

class Vital_data:
    def __init__(self, id : int, tmstp : str, bpm : int, body_temperature : float, body_pressure : int, bed_id : int):
        self.id = id
        self.tmstp = tmstp
        self.bpm = bpm
        self.body_temperature = body_temperature
        self.body_pressure = body_pressure
        self.bed_id = bed_id

vital_data_blueprint = Blueprint('vital_data', __name__)