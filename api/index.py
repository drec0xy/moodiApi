from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Home 🚀🚀🚀'

@app.route('/about')
def about():
    return 'About'

@app.route('/infere/<inference>', ['GET'])
def infer(inference):
    return jsonify(userQuery = "can you do something for me?", botResponds = "Sure what is that?",queryTimestamp = "2013-10-21T13:28:06.419Z",respondTimestamp = "2013-10-21T13:28:06.419Z")