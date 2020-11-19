from typing import Tuple
import os.path
import requests
import json

SETTINGS_FILE_NAME = "settings.cfg"
PROTOCOL = "http://"
ENPOINT_ROOM = "/room"

def settings_exits() -> bool:
    return os.path.isfile(SETTINGS_FILE_NAME)

def load_settings() -> Tuple[str, int]:
    with open(SETTINGS_FILE_NAME) as settings_file:
        settings = json.load(settings_file)
        return (settings["server_host"], settings["room_id"])

def save_settings(server_host : str, room_id : int) -> None:
    settings = {}
    settings["server_host"] = server_host
    settings["room_id"] = room_id

    with open(SETTINGS_FILE_NAME, "w") as settings_file:
        json.dump(settings, settings_file)

def change_settings():
    server_host = input("Server IP address: " + PROTOCOL)
    server_host = PROTOCOL + server_host
    response = requests.get(server_host)

    if response.status_code == 200:
        rooms = requests.get(server_host + ENPOINT_ROOM + "/all")
        if rooms is not None:
            try:
                rooms_json = rooms.json()
            except ValueError:
                print("ERROR: Bad response")
                exit()

            count = 0
            for room in rooms_json:
                print("%d) %s" % (count, room["name_room"]))
                count += 1

            chosen_room = int(input("Choose a room by its number: "))
            try:
                room = rooms_json[chosen_room]
                room_id = room["id"]
                save_settings(server_host, room_id)
                print("\n*SETUP COMPLETED*")
            except IndexError:
                print("ERROR: The room doesn't exits")
    else:
        print("ERROR: The server can't be reached")


if settings_exits():
    saved_server_host, saved_room_id = load_settings()
    print("*CURRENT SETTINGS*")
    print("Server IP address: " + saved_server_host)
    print("Room id: %d" % (saved_room_id))
    change = input("Would you like to change it? [y/n]: ").lower()[0]
    print("\n")
    if change == 'y':
        change_settings()
else:
    change_settings()




