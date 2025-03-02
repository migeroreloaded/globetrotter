import React, { useState } from "react";
import axios from "axios";

function Register() {
  const [username, setUsername] = useState("");
  const [message, setMessage] = useState("");

  const handleRegister = async () => {
    try {
      const response = await axios.post("https://globetrotter-j9g8.onrender.com/user/register", { username });
      setMessage(response.data.message);

      // Store username in session storage upon successful registration
      sessionStorage.setItem("username", username);
    } catch (error) {
      const errorMessage = error.response?.data?.error || "Registration failed";

      // Check if the error message indicates the username is already taken
      if (errorMessage.toLowerCase().includes("username taken")) {
        sessionStorage.setItem("username", username);
        alert(`Logged in as ${username}`);
      }

      setMessage(errorMessage);
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <input
        type="text"
        placeholder="Enter username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <button onClick={handleRegister}>Register</button>
      <p>{message}</p>
    </div>
  );
}

export default Register;
