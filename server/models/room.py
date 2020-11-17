from flask import Blueprint

class Room:
    def __init__(self, id : int, name : str):
        self.id = id
        self.name = name

room_blueprint = Blueprint('room', __name__)