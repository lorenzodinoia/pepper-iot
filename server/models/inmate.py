import os
import mysql.connector
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

class Inmate:
    def __init__(self, id : int, name : str, surname : str, CF : str, date_birth : str):
        self.id = id
        self.name = name
        self.surname = surname
        self.CF = CF
        self.date_birth = date_birth

inmate_blueprint = Blueprint('inmate', __name__)