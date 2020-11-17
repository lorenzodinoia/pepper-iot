from flask import Flask
from flask import jsonify
from models.data import data_blueprint
from models.room import room_blueprint

DATA_API_PREFIX = "/data"
ROOM_API_PREFIX = "/room"

app = Flask(__name__) #Server instance

app.register_blueprint(data_blueprint, url_prefix=DATA_API_PREFIX)
app.register_blueprint(room_blueprint, url_prefix=ROOM_API_PREFIX)

@app.route("/") #Home page route
def home():
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) #Run server
