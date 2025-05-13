import pytest
import json
from app import create_app, db
from app.models import User, Task

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = User(username="test", password="test")
            db.session.add(user)
            db.session.commit()
        yield client

def test_register(client):
    response = client.post('/register', json={"username": "user1", "password": "pass1"})
    assert response.status_code == 201

def test_login(client):
    response = client.post('/login', json={"username": "test", "password": "test"})
    assert 'access_token' in response.get_json()
