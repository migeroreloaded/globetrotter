import axios from "axios";

const API_BASE_URL = "https://globetrotter-j9g8.onrender.com";

export const registerUser = async (username) => {
  return axios.post(`${API_BASE_URL}/user/register`, { username });
};

export const acceptChallenge = async (inviteId, username) => {
  return axios.post(`${API_BASE_URL}/challenge/accept`, { invite_id: inviteId, username });
};
