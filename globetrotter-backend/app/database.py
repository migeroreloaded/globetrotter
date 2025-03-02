from app import create_app, db
from app.models import Destination

data = [
    {
        "city": "Paris",
        "country": "France",
        "clues": [
            "This city is home to a famous tower that sparkles every night.",
            "Known as the 'City of Love' and a hub for fashion and art."
        ],
        "fun_fact": [
            "The Eiffel Tower was supposed to be dismantled after 20 years but was saved because it was useful for radio transmissions!",
            "Paris has only one stop sign in the entire city—most intersections rely on priority-to-the-right rules."
        ],
        "trivia": [
            "This city is famous for its croissants and macarons. Bon appétit!",
            "Paris was originally a Roman city called Lutetia."
        ]
    }
]

app = create_app()

with app.app_context():
    db.create_all()
    for item in data:
        destination = Destination(
            city=item["city"],
            country=item["country"],
            clues=item["clues"],
            fun_fact=item["fun_fact"],
            trivia=item["trivia"]
        )
        db.session.add(destination)
    db.session.commit()
    print("Database seeded!")
