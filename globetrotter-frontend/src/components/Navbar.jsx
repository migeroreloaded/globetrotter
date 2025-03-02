import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="/register">Register</Link>
      <Link to="/game">Play Game</Link>
      <Link to="/challenge">Challenge</Link>
    </nav>
  );
}

export default Navbar;
