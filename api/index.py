from flask import Flask,jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return 'Home 🚀🚀🚀'

@app.route('/about')
def about():
    return 'About'

@app.route('/infere/<inference>')
def infer(inference):
    return jsonify(userQuery = inference, botResponds = "please comeback soon, Moodichatbot is still under developement.",queryTimestamp = "2013-10-21T13:28:06.419Z",respondTimestamp = datetime.now())


if __name__ == '__main__':
    app.run()