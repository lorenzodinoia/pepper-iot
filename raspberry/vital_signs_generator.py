import time
import random
import requests
import json

file = json.loads(open("settings_vs.cfg", "r").read())
server_host = file["server_host"]
bed_id = file["bed_id"]

while True:
    bpm = random.randint(60, 100)
    body_temperature = random.randint(350, 375) / 10
    min_body_pressure = random.randint(60, 80)
    max_body_pressure = random.randint(105, 120)
    blood_oxygenation = random.randint(90, 100)

    payload = {"bpm" : bpm, "body_temperature" : body_temperature, "min_body_pressure" : min_body_pressure, "max_body_pressure" : max_body_pressure, "blood_oxygenation" : blood_oxygenation, "bed_id" : bed_id}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(server_host + "/vital_signs/add", json.dumps(payload), headers=headers)
    if response.status_code != 200:
        print("Errore")
    else:
        data = response.json()
        print(data)
    
    time.sleep(60)