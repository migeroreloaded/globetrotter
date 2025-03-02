import React, { useState } from "react";
import axios from "axios";

function Challenge() {
  const [username, setUsername] = useState("");
  const [message, setMessage] = useState("");
  const [shareableLink, setShareableLink] = useState("");
  const [loading, setLoading] = useState(false); // New loading state

  const createChallenge = async () => {
    if (!username) {
      setMessage("Please enter a username.");
      return;
    }
    
    setMessage(""); // Clear previous error messages
    setLoading(true); // Set loading to true while request is in progress

    try {
      const response = await axios.post("https://globetrotter-j9g8.onrender.com/challenge", { username });

      if (response.data.invite_link) {
        setShareableLink(response.data.invite_link); // Correctly setting the invite link
        setMessage(`Challenge created! Share this link: ${response.data.invite_link}`);
      } else {
        setMessage("Unexpected response format from the server.");
      }
    } catch (error) {
      setMessage(error.response?.data?.error || "Failed to create challenge");
      console.error("Error creating challenge:", error.response || error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Challenge a Friend</h2>
      <input 
        type="text" 
        placeholder="Enter your username" 
        value={username} 
        onChange={(e) => setUsername(e.target.value)} 
      />
      <button onClick={createChallenge} disabled={loading}>
        {loading ? "Generating..." : "Generate Invite"}
      </button>
      
      {shareableLink && (
        <div>
          <p>Share this link with a friend:</p>
          <a href={shareableLink} target="_blank" rel="noopener noreferrer">{shareableLink}</a>
        </div>
      )}
      
      {message && <p>{message}</p>} {/* Display message */}
    </div>
  );
}

export default Challenge;
