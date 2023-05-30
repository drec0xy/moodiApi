from flask import Flask,jsonify
from datetime import datetime
from flask_cors import CORS

from inferer import generate_answer

app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return 'Home 🚀🚀🚀'

@app.route('/about')
def about():
    return 'About'

@app.route('/infere/<inference>')
def infer(inference):
    return jsonify(userQuery = inference, botResponds = "Sorry I'm still kinda dumb right now 🤪, Afte my training I'd be super smart,I'd answer all of your questions soon😎😁😜",queryTimestamp = "2013-10-21T13:28:06.419Z",respondTimestamp = datetime.now())


@app.route('/<query>')
def inference(query):
    return jsonify(userQuery = query, botResponds = generate_answer(query), queryTimestamp = "2013-10-21T13:28:06.419Z",respondTimestamp = datetime.now())


if __name__ == '__main__':
    app.run(debug=True, port=8000)