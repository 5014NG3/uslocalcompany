from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import pandas as pd

DATABASE = 'us_sba.db'

valid_cities = set(pd.read_csv("./valid_business_data/valid_cities.csv")["actual_city"])
valid_states = set(pd.read_csv("./valid_business_data/valid_states.csv")["state"])

app = Flask(__name__)
CORS(app)  

def get_db_connection():
    conn = sqlite3.connect('sbdata.db')
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.close()
    conn = sqlite3.connect('file:sbdata.db?mode=ro', uri=True)
    return conn


class Config:
    DEBUG = True
    JSON_SORT_KEYS = False
    
app.config.from_object(Config)

# Basic health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Server is running'
    })

# Example route with parameters
@app.route('/api/hello/<name>', methods=['GET'])
def hello(name):
    return jsonify({
        'message': f'Hello, {name}!'
    })

@app.route('/api/<state>')
def index(state):

    if state not in valid_states:
        return jsonify([])


    city = ""
    if 'city' in request.args:
        city = request.args['city']
        if city not in valid_cities:
            return jsonify([])


    offset = 0
    if 'offset' in request.args:
        offset = request.args['offset']
        if offset.isdigit():
            offset = int(offset)
        else:
            offset = 0

    state = str(state).upper()
    results = query_db("SELECT * FROM sba WHERE state = ? AND actual_city = ? ORDER BY zip LIMIT 20 OFFSET ?;", (state,city,offset,), one=False)
    columns = ["view","firm_name","person","title","address_line_1","address_line_2","city","state","zip","capabilities","email","website","area","plusfour","full_zip","actual_city"]
    json_data = []
    for row in results:
        business_dict = dict(zip(columns, row))
        json_data.append(business_dict)

    
    return jsonify(json_data)


def query_db(query, args=(), one=False):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)