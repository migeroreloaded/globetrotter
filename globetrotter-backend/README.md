# Globetrotter - The Ultimate Travel Guessing Game

Welcome to **Globetrotter**, the ultimate guessing game where you can test your knowledge of famous destinations around the world! In this game, players are presented with cryptic clues about a famous location and must guess the correct destination.

## Features
- **Game Questions**: Players are given clues about a destination and must choose the correct city.
- **Dynamic Feedback**: Instant feedback with fun animations, showing whether the answer was correct or not.
- **Score Tracking**: Players' scores are tracked, with the ability to challenge friends.
- **Challenge a Friend**: Players can challenge a friend to play and compare scores via a dynamic invite link.
- **AI-powered Dataset**: AI is used to generate additional clues, fun facts, and trivia for destinations.

## Prerequisites

Before you begin, ensure that you have the following installed:

- Python 3.x
- pip (Python package installer)
- OpenAI API key (if using AI functionality)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/globetrotter.git
    cd globetrotter
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
    
      ```bash
      venv\Scripts\activate
      ```

    - On MacOS/Linux:
    
      ```bash
      source venv/bin/activate
      ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up environment variables:
   Create a `.env` file in the root directory of the project with the following content:

    ```
    DATABASE_URL=sqlite:///globetrotter.db
    SECRET_KEY=your_secret_key
    OLLAMA_API_URL=http://localhost:11434/api/generate
    ```

6. Initialize the database:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

7. Run the app:

    ```bash
    python run.py
    ```

    The Flask app should now be running on `http://127.0.0.1:5000/`.

## Usage

- To create a user, send a `POST` request to `/user/register` with the `username` field in the JSON payload.
- To play the game, send a `GET` request to `/game/question` for a random question.
- To submit an answer, send a `POST` request to `/game/answer` with the `answer`, `destination_id`, and `username`.
- To create a challenge, send a `POST` request to `/challenge` with the `username` field.
- To accept a challenge, send a `POST` request to `/challenge/accept` with the `invite_id` and `username`.

## Testing

To run the tests using `pytest`, use the following command:

```bash
pytest
