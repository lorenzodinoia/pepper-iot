import os
import constants
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort
from flask import json
import mysql.connector

class Emergency:
    def __init__(self, id : int ,timestamp : str, bed_id : int, environmental_data_id : int, vital_signs_id : int):
        self.id = id
        self.timestamp = timestamp
        self.bed_id = bed_id
        self.environmental_data_id = environmental_data_id
        self.vital_signs_id = vital_signs_id

emergency_blueprint = Blueprint('emergency', __name__)
