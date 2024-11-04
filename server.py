from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
from flask import g


DATABASE = 'us_sba.db'

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
    results = query_db("SELECT * FROM businesses WHERE state = ?", (state,), one=False)


    columns = ["index","view","firm_name","person","title","address_line_1","address_line_2","city","state","zip","capabilities","email","website","area","plusfour"]
    json_data = [{"len" : str(len(results)) }]
    for row in results:
        business_dict = dict(zip(columns, row))
        json_data.append(business_dict)
    
    return jsonify(json_data)


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)