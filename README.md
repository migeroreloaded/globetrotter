# Globetrotter Challenge

Globetrotter Challenge is a travel guessing game where users try to identify locations based on images, descriptions, or other clues. This project consists of a **backend** (Flask) and a **frontend** (React) working together to deliver an engaging experience.

## Features

- Interactive location-guessing game
- Backend API for managing game logic and data
- Frontend UI for user interaction and gameplay
- Deployment-ready setup for both frontend and backend

## Project Structure

``` sh
/globetrotter-challenge
│── backend/      # Flask backend
│── frontend/     # React frontend
│── README.md     # Project documentation
```

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Node.js and npm
- Flask and required Python dependencies

## Setup

### Backend Setup

1. Navigate to the backend folder:

   ```sh
   cd backend
   ```

2. Create a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the backend server:

   ```sh
   flask run
   ```

### Frontend Setup

1. Navigate to the frontend folder:

   ```sh
   cd frontend
   ```

2. Install dependencies:

   ```sh
   npm install
   ```

3. Start the frontend:

   ```sh
   npm start
   ```

## Deployment

For deployment, ensure that both frontend and backend are hosted properly. You can use services like:

- **Backend**: Render, Heroku, or AWS
- **Frontend**: Vercel or Netlify

## Contribution

Feel free to fork this repository and submit pull requests. Any contributions to improve the game are welcome!

## License

This project is licensed under the MIT License.
