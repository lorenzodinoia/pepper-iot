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
        return (settings["server_host"], settings["room_id"], settings["room_name"])

def save_settings(server_host : str, room_id : int, room_name : str) -> None:
    settings = {}
    settings["server_host"] = server_host
    settings["room_id"] = room_id
    settings["room_name"] = room_name

    with open(SETTINGS_FILE_NAME, "w") as settings_file:
        json.dump(settings, settings_file)

def change_settings():
    server_host = input("Server IP address: " + PROTOCOL)
    server_host = PROTOCOL + server_host
    response = requests.get(server_host)

    if response.status_code == 200:
        rooms = requests.get(server_host + ENPOINT_ROOM + "/list")
        if rooms is not None:
            try:
                rooms_json = rooms.json()
            except ValueError:
                print("ERROR: Bad response")
                exit()

            if len(rooms_json) > 0:
                count = 1
                for room in rooms_json:
                    print("%d) %s" % (count, room["name"]))
                    count += 1
                chosen_room = int(input("Choose a room by its number: "))
                try:
                    room = rooms_json[chosen_room - 1]
                    save_settings(server_host, room["id"], room["name"])
                    print("\n*SETUP COMPLETED*")
                except IndexError:
                    print("ERROR: The room doesn't exits")
            else:
                print("*NO ROOMS AVAILBALE*")
    else:
        print("ERROR: The server can't be reached")

#Running code
if settings_exits():
    saved_server_host, saved_room_id, saved_room_name = load_settings()
    print("*CURRENT SETTINGS*")
    print("Server IP address: " + saved_server_host)
    print("Room: %d - %s" % (saved_room_id, saved_room_name))
    change = input("Would you like to change it? [y/n]: ").lower()[0]
    print("\n")
    if change == 'y':
        change_settings()
else:
    change_settings()