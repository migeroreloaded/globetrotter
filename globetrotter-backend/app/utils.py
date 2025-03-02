import ollama
import re
import json
import time
from app import db
from app.models import Destination

destinations = [
    "New York", "London", "Tokyo", "Paris", "Rome"
]  # Keep it short for testing; expand later.

def extract_json(raw_text):
    """Extracts the first valid JSON object from a response containing extra data."""
    json_match = re.search(r'\{.*?\}', raw_text, re.DOTALL)
    return json_match.group(0) if json_match else None

def generate_destination_data(destination_name):
    """Generates clues, fun facts, and trivia for a given destination using Ollama."""

    prompt = f"""
    Provide **only** a valid JSON object (not an array), without any explanations.
    Ensure it follows this format:
    {{
        "clues": ["..."],
        "fun_facts": ["..."],
        "trivia": ["..."]
    }}
    """

    try:
        response = ollama.chat(
            model="tinyllama",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_text = response["message"]["content"].strip()
        print(f"Raw Response for {destination_name}:\n{raw_text}")

        # Extract JSON object
        json_text = extract_json(raw_text)
        if not json_text:
            print(f"❌ No valid JSON detected for {destination_name}")
            return None

        # Parse JSON
        data = json.loads(json_text)

        # Validate expected keys exist
        if not all(key in data for key in ["clues", "fun_facts", "trivia"]):
            print(f"❌ Incomplete JSON for {destination_name}")
            return None

        return data

    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error for {destination_name}: {str(e)}")
    except Exception as e:
        print(f"❌ Error generating data for {destination_name}: {str(e)}")

    return None

def populate_database():
    """Populates the database with AI-generated data for multiple destinations."""

    for city in destinations:
        if Destination.query.filter_by(city=city).first():
            print(f"Skipping {city} (Already exists in DB)")
            continue

        print(f"Generating data for {city}...")
        data = generate_destination_data(city)

        if data:
            try:
                new_destination = Destination(
                    city=city,
                    country="Unknown",
                    clues=data.get("clues", []),
                    fun_fact=data.get("fun_facts", []),
                    trivia=data.get("trivia", [])
                )

                db.session.add(new_destination)
                db.session.commit()
                print(f"✅ Added {city} to database.")

            except Exception as e:
                db.session.rollback()
                print(f"❌ Database error for {city}: {str(e)}")

        time.sleep(1)  # Prevent excessive API calls

    print("✅ Database population complete!")

if __name__ == "__main__":
    with db.session.begin():
        populate_database()
