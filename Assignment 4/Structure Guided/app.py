from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Routes to serve JSON data for Used Cars, New Cars, and Bikes
@app.route('/used-cars')
def get_used_cars():
    with open('used_cars.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/new-cars')
def get_new_cars():
    with open('new_cars.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/bikes')
def get_bikes():
    with open('bikes.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

# Route to render the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
