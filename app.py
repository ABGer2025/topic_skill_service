import os
import uuid
from flask import Flask, jsonify, request
from data_manager import JsonDataManager

app = Flask(__name__)
data_manager = JsonDataManager()

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
TOPICS_FILE = os.path.join(DATA_DIR, 'topics.json')
SKILLS_FILE = os.path.join(DATA_DIR, 'skills.json')


@app.route('/')
def hello_world():
    return 'Hello from Topic and Skill Service!'


@app.route('/topics', methods=['GET'])
def get_topics():
    topics = data_manager.read_data(TOPICS_FILE)
    return jsonify(topics)


@app.route('/skills', methods=['GET'])
def get_skills():
    skills = data_manager.read_data(SKILLS_FILE)
    return jsonify(skills)


@app.route('/topics/<id>', methods=['GET'])
def get_topic_by_id(id):
    topics = data_manager.read_data(TOPICS_FILE)
    topic = next((topic for topic in topics if topic.get('id').lower() == id.lower()), None)
    if topic:
        return jsonify(topic)
    else:
        return jsonify({"error": "Topic not found."}), 404


@app.route('/skills/<id>', methods=['GET'])
def get_skill_by_id(id):
    skills = data_manager.read_data(SKILLS_FILE)
    skill = next((skill for skill in skills if skill.get('id').lower() == id.lower()), None)
    if skill:
        return jsonify(skill)
    else:
        return jsonify({"error": "Skill not found."}), 404
    

@app.route('/topics', methods=['POST'])
def create_topic():
    new_topic_data = request.json

    if not new_topic_data or 'name' not in new_topic_data or 'description' not in new_topic_data:
        return jsonify({"error": "'name' and 'description' for the topic are required in the request body."}), 400

    new_topic_id = str(uuid.uuid4())

    topic = {
        "id": new_topic_id,
        "name": new_topic_data['name'],
        "description": new_topic_data['description']
    }

    topics = data_manager.read_data(TOPICS_FILE)
    topics.append(topic)

    data_manager.write_data(TOPICS_FILE, topics)

    return jsonify(topic), 201


@app.route('/skills', methods=['POST'])
def create_skill():
    new_skill_data = request.json

    if not new_skill_data or 'name' not in new_skill_data or 'topicId' not in new_skill_data:
        return jsonify({"error": "'name' and 'topicId' for the topic are required in the request body."}), 400

    new_skill_id = str(uuid.uuid4())

    skill = {
        "id": new_skill_id,
        "name": new_skill_data['name'],
        "topicId": new_skill_data['topicId'],
        "difficulty": new_skill_data.get('difficulty', 'unknown')}


    skills = data_manager.read_data(SKILLS_FILE)
    skills.append(skill)

    data_manager.write_data(SKILLS_FILE, skill)

    return jsonify(skill), 201


@app.route('/topics/<id>', methods=['PUT'])
def update_topic(id):
    updated_data = request.json

    if not updated_data or 'name' not in updated_data or 'description' not in updated_data:
        return jsonify({"error": "Name und Beschreibung für das Topic sind erforderlich"}), 400

    topics = data_manager.read_data(TOPICS_FILE)

    found_index = -1
    for i, t in enumerate(topics):
        if t['id'] == id:
            found_index = i
            break

    if found_index == -1:
        return jsonify({"error": "Topic not found"}), 404

    topics[found_index]['name'] = updated_data['name']
    topics[found_index]['description'] = updated_data['description']
  
    data_manager.write_data(TOPICS_FILE, topics)

    return jsonify(topics[found_index]), 200      

if __name__ == '__main__':
    app.run(debug=True, port=5000)