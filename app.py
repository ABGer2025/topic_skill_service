import json
import os
from flask import Flask, jsonify


app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
TOPICS_FILE = os.path.join(DATA_DIR, 'topics.json')


@app.route('/')
def hello_world():
    return 'Hello from Topic and Skill Service! How are you today?'

def read_json_file(filepath):
    if not os.path.exists(filepath):
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Fehler beim Dekodieren der JSON-Datei: {filepath}. Bitte JSON-Syntax überprüfen!")
        return[]
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist beim lesen von: {filepath}: {e} aufgetreten!")
        return[]
    
    @app.route('/topics', method='GET')
    def get_topics():
        topics = read_json_file(TOPICS_FILE)
        return jsonify (topics)
    


if __name__ == '__main__':
    app.run(debug=True, port=5000)