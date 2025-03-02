import { useParams } from "react-router-dom";
import { useState } from "react";
import axios from "axios";

function ChallengePage() {
  const { id } = useParams(); // Get invite ID from URL
  const [username, setUsername] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [challengeData, setChallengeData] = useState(null);

  const acceptChallenge = async () => {
    if (!username) {
      setMessage("Please enter a username.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await axios.post("http://localhost:5000/challenge/accept", {
        invite_id: id,
        username: username
      });

      setChallengeData(response.data);
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.error || "Failed to accept challenge.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Accept Challenge</h2>
      <p>Enter your username to accept the challenge:</p>
      <input 
        type="text" 
        placeholder="Enter your username" 
        value={username} 
        onChange={(e) => setUsername(e.target.value)} 
      />
      <button onClick={acceptChallenge} disabled={loading}>
        {loading ? "Accepting..." : "Accept Challenge"}
      </button>

      {message && <p>{message}</p>}

      {challengeData && (
        <div>
          <h3>Challenge Details</h3>
          <p>Inviter's Score: {challengeData.inviter_score}</p>
          <p>Your Score: {challengeData.invitee_score}</p>
        </div>
      )}
    </div>
  );
}

export default ChallengePage;
