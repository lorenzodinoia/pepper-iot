import os
import constants
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

bed_blueprint = Blueprint('bed', __name__)
