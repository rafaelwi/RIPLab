import time
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

cors = CORS(app, resources={'/*':{'origins': 'http://localhost:3000'}}) 

if __name__ == "__main__":
    app.run()
