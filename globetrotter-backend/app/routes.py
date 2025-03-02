from flask import Blueprint, jsonify, request
import json
from app.models import Destination, User, Challenge, db
import random

routes = Blueprint("routes", __name__)

# Get a random destination with clues
@routes.route("/game/question", methods=["GET"])
def get_random_question():
    destinations = Destination.query.all()
    if not destinations:
        return jsonify({"error": "No destinations found"}), 404

    destination = random.choice(destinations)
    clues_list = json.loads(destination.clues) if isinstance(destination.clues, str) else destination.clues
    clues = random.sample(clues_list, min(2, len(clues_list)))
    fun_fact = random.choice(json.loads(destination.fun_fact)) if isinstance(destination.fun_fact, str) else destination.fun_fact

    
    other_cities = [d.city for d in Destination.query.all() if d.city != destination.city]

    if len(other_cities) < 3:
        options = [destination.city] + random.sample(other_cities, len(other_cities))  # Use all available cities
    else:
        options = [destination.city] + random.sample(other_cities, 3)  # Select 3 as intended

    random.shuffle(options)
    
    question_data = {
        "destination_id": destination.id,
        "clues": clues,
        "options": options,
        "correct_answer": destination.city,  # Send correct answer
        "fun_fact": fun_fact
    }
    return jsonify(question_data)

# Check answer and update score
@routes.route("/game/answer", methods=["POST"])
def check_answer():
    data = request.json
    print("Received Data:", data)  # Debugging
    user_answer = data.get("answer")
    destination_id = data.get("destination_id")
    username = data.get("username")

    destination = Destination.query.get(destination_id)
    user = User.query.filter_by(username=username).first()

    if not destination or not user:
        return jsonify({"error": "Invalid data"}), 400

    # Check if the user's answer is correct
    correct = user_answer.lower() == destination.city.lower()

    # Update score if correct
    if correct:
        user.score += 1
        db.session.commit()

    fun_fact = json.loads(destination.fun_fact) if isinstance(destination.fun_fact, str) else destination.fun_fact
    fun_fact = random.choice(fun_fact)

    return jsonify({
        "correct": correct,
        "fun_fact": fun_fact,
        "feedback": "🎉 Correct! Confetti animation!" if correct else "😢 Incorrect! Sad-face animation!",
        "updated_score": user.score
    })


# Register user
@routes.route("/user/register", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username taken"}), 400

    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered", "username": username}), 201

# Create a challenge link
@routes.route("/challenge", methods=["POST"])
def create_challenge():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user:
        new_user = User(username=username, score=0)  # Assign default score of 0
        db.session.add(new_user)
        db.session.commit()
        user = new_user  # Assign the new user to 'user' variable

    challenge = Challenge(
        inviter_username=user.username,
        inviter_score=user.score  # Store the inviter's score
    )
    db.session.add(challenge)
    db.session.commit()

    invite_link = f"http://localhost:5173/challenge/{challenge.id}"
    
    return jsonify({"message": "Challenge created", "invite_link": invite_link, "score": user.score})

# Accept a challenge (invitee clicks link)
@routes.route("/challenge/accept", methods=["POST"])
def accept_challenge():
    data = request.json
    invite_id = data.get("invite_id")
    username = data.get("username")

    # Check if challenge exists
    challenge = Challenge.query.get(invite_id)
    if not challenge:
        return jsonify({"error": "Challenge not found"}), 404

    # Check if the challenge has already been accepted
    if challenge.invitee_username:
        return jsonify({"error": "Challenge already accepted"}), 400

    # Check if user exists; if not, create the user
    invitee = User.query.filter_by(username=username).first()
    if not invitee:
        invitee = User(username=username, score=0)  # Default score is 0
        db.session.add(invitee)
        db.session.commit()

    # Assign invitee to challenge and update status
    challenge.invitee_username = username
    challenge.invitee_status = "accepted"
    db.session.commit()

    return jsonify({
        "message": "Challenge accepted!",
        "inviter_score": challenge.inviter_score,
        "invitee_score": invitee.score
    })
