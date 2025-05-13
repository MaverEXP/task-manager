from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app import app, db
from .models import User, Task
from .utils import send_email

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{"title": t.title, "completed": t.completed} for t in tasks])

@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    task = Task(title=data['title'], user_id=get_jwt_identity())
    db.session.add(task)
    db.session.commit()
    send_email("New task created", f"Task: {data['title']}")
    return jsonify({"message": "Task created"}), 201
