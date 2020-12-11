import os
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

class Doctor:
    def __init__(self, id : int, name : str, surname : str, CF : str, ward_id : int):
        self.id = id
        self.name = name
        self.surname = surname
        self.CF = CF
        self.ward_id = ward_id

doctor_blueprint = Blueprint('doctor', __name__)