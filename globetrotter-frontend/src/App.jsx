import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Register from "./pages/Register";
import Game from "./pages/Game";
import Challenge from "./pages/Challenge";
import ChallengePage from "./pages/ChallengePage";
import Navbar from "./components/Navbar";

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/game" element={<Game />} />
        <Route path="/challenge" element={<Challenge />} />
        <Route path="/challenge/:id" element={<ChallengePage />} />
      </Routes>
    </div>
  );
}

export default App;
