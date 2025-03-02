import pytest
from app import create_app, db
from app.models import User, Destination, Challenge
from app.utils import generate_destination_data
import random

@pytest.fixture
def client():
    app = create_app("testing")
    client = app.test_client()
    
    with app.app_context():
        db.create_all()
    
    yield client

    with app.app_context():
        db.drop_all()

def test_register_user(client):
    response = client.post("/user/register", json={"username": "testuser"})
    assert response.status_code == 200
    assert response.json["message"] == "User registered"

def test_get_question(client):
    destination = Destination(city="Paris", country="France", clues=["Eiffel Tower"], fun_fact=["City of Love"], trivia=["Capital of France"])
    
    with client.application.app_context():
        db.session.add(destination)
        db.session.commit()

    response = client.get("/game/question")
    assert response.status_code == 200
    assert "clues" in response.json

def test_check_answer(client):
    with client.application.app_context():
        destination = Destination(city="Paris", country="France", clues=["Eiffel Tower"], fun_fact=["City of Love"], trivia=["Capital of France"])
        user = User(username="testuser", score=0)
        db.session.add(destination)
        db.session.add(user)
        db.session.commit()

    response = client.post("/game/answer", json={
        "username": "testuser",
        "destination_id": destination.id,
        "answer": "Paris"
    })
    assert response.status_code == 200
    assert response.json["correct"] is True
    assert "fun_fact" in response.json

def test_create_challenge(client):
    with client.application.app_context():
        user = User(username="testuser", score=5)
        db.session.add(user)
        db.session.commit()
    
    response = client.post("/challenge", json={"username": "testuser"})
    assert response.status_code == 200
    assert "invite_link" in response.json
    assert response.json["score"] == 5
    assert "inviter_score" in response.json["invite_link"]

def test_accept_challenge(client):
    with client.application.app_context():
        inviter = User(username="inviter", score=10)
        invitee = User(username="invitee", score=5)
        db.session.add(inviter)
        db.session.add(invitee)
        db.session.commit()

        challenge = Challenge(
            inviter_username="inviter",
            inviter_score=10
        )
        db.session.add(challenge)
        db.session.commit()

    response = client.post("/challenge/accept", json={
        "invite_id": challenge.id,
        "username": "invitee"
    })
    assert response.status_code == 200
    assert response.json["message"] == "Challenge accepted!"
    assert response.json["inviter_score"] == 10
    assert response.json["invitee_score"] == 5

def test_accept_challenge_already_accepted(client):
    with client.application.app_context():
        inviter = User(username="inviter", score=10)
        invitee = User(username="invitee", score=5)
        db.session.add(inviter)
        db.session.add(invitee)
        db.session.commit()

        challenge = Challenge(
            inviter_username="inviter",
            inviter_score=10,
            invitee_username="invitee",  # Mark as already accepted
            invitee_status="accepted"
        )
        db.session.add(challenge)
        db.session.commit()

    response = client.post("/challenge/accept", json={
        "invite_id": challenge.id,
        "username": "invitee"
    })
    assert response.status_code == 400
    assert response.json["error"] == "Challenge already accepted"

def test_invalid_challenge(client):
    response = client.post("/challenge/accept", json={
        "invite_id": "invalid_id",
        "username": "invitee"
    })
    assert response.status_code == 400
    assert response.json["error"] == "Challenge not found"

def test_ai_dataset_expansion(client):
    destination_name = "Berlin"
    generated_data = generate_destination_data(destination_name)
    
    with client.application.app_context():
        new_destination = Destination(
            city=destination_name,
            country="Germany",
            clues=generated_data["clues"],
            fun_fact=generated_data["fun_facts"],
            trivia=generated_data["trivia"]
        )
        db.session.add(new_destination)
        db.session.commit()
    
        stored_destination = Destination.query.filter_by(city=destination_name).first()
        assert stored_destination is not None
        assert len(stored_destination.clues) > 0
        assert len(stored_destination.fun_fact) > 0
        assert len(stored_destination.trivia) > 0
