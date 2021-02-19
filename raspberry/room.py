#import Adafruit_DHT
import time
import random
import requests
import json

file = json.loads(open("settings.cfg", "r").read())

while True:
    
    #humidity, degree = Adafruit_DHT.read_retry(11, 4)
    humidity = random.randint(0, 60)
    degree = random.randint(15, 30)
    voc = (random.randint(0,7))/10.0
    lux = random.randint(401, 1000)
    payload = {"lux" : lux, "voc" : voc, "degree" : degree, "humidity" : humidity, "room_id" : file["room_id"]}
    url = file["server_host"] + "/env_data/add"
    response = requests.post(url, json = payload)
    if response.status_code != 200:
        print("Errore")
    else:
        data = response.json()
        print(data)
    
    time.sleep(300)
