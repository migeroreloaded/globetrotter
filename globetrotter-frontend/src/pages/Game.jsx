import React, { useState, useEffect } from "react";
import axios from "axios";
import Confetti from "react-confetti";

function Game() {
  const [question, setQuestion] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [funFact, setFunFact] = useState(null);
  const [score, setScore] = useState(0);
  const [showConfetti, setShowConfetti] = useState(false);
  const [answered, setAnswered] = useState(false); // Track answer state

  useEffect(() => {
    fetchQuestion();
  }, []);

  const fetchQuestion = async () => {
    try {
      const response = await axios.get("https://globetrotter-j9g8.onrender.com/game/question");
      setQuestion(response.data);
      setFeedback(null);
      setFunFact(null);
      setAnswered(false);
    } catch (error) {
      console.error("Error fetching question:", error);
    }
  };

  const checkAnswer = async (answer) => {
    if (answered) return; // Prevent multiple clicks
    setAnswered(true);

    const username = sessionStorage.getItem("username");

    const response = await axios.post("https://globetrotter-j9g8.onrender.com/game/answer", {
      answer,
      destination_id: question.destination_id,
      username
    });

    setFeedback(response.data.correct ? "🎉 Correct!" : "😢 Incorrect!");
    setFunFact(response.data.fun_facts);

    if (response.data.correct) {
      setScore((prevScore) => prevScore + 1);
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 3000);
    }
  };

  return (
    <div className="game-container">
      <h2>Guess the Destination</h2>
      {showConfetti && <Confetti />}
      {question ? (
        <div>
          <p>{question.clues.join(" ")}</p>
          {question.options.map((option, index) => (
            <button key={index} onClick={() => checkAnswer(option)} disabled={answered}>
              {option}
            </button>
          ))}
          {feedback && (
            <div className={`feedback ${feedback.includes("Correct") ? "correct" : "incorrect"}`}>
              <p>{feedback}</p>
              <p className="fun-fact">{funFact}</p>
            </div>
          )}
          {answered && <button onClick={fetchQuestion}>Next Question</button>}
        </div>
      ) : (
        <p>Loading...</p>
      )}
      <p>Score: {score}</p>
    </div>
  );
}

export default Game;
