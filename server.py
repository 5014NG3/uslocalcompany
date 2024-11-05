from flask import Flask, jsonify
from flask_cors import CORS
from flask import g
import os
import psycopg2

DATABASE = 'us_sba.db'

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user="postgres",
                            password="123")
    
    return conn


# Basic configuration
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
    state = str(state).upper()
    results = query_db("SELECT * FROM public.usa_sba WHERE state = %s;", (state,), one=False)
    columns = ["index","view","firm_name","person","title","address_line_1","address_line_2","city","state","zip","capabilities","email","website","area","plusfour","full_zip","actual_city"]
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