import time
import random
import requests
import json

file = json.loads(open("settings_vs.cfg", "r").read())
server_host = file["server_host"]
urldest = ("""/bed?id=%d""" %  (file["bed_id"]))
url = server_host + urldest
bed = requests.get(url)
bed_json = bed.json()
if len(bed_json) > 0:
    inmate_id = bed_json[0]["inmate_id"]
else:
    inmate_id = None
print(inmate_id)

if(inmate_id is not None):
    while True:
        bpm = random.randint(60, 100)
        body_temperature = random.randint(350, 375) / 10
        min_body_pressure = random.randint(60, 80)
        max_body_pressure = random.randint(105, 120)
        blood_oxygenation = random.randint(90, 100)

        payload = {"bpm" : bpm, "body_temperature" : body_temperature, "min_body_pressure" : min_body_pressure, "max_body_pressure" : max_body_pressure, "blood_oxygenation" : blood_oxygenation, "inmate_id" : inmate_id}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(server_host + "/vital_signs/add", json.dumps(payload), headers=headers)
        if response.status_code != 200:
            print("Errore")
        else:
            data = response.json()
            print(data)
        
        time.sleep(60)