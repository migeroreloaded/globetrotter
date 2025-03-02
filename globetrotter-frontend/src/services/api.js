import axios from "axios";

const API_BASE_URL = "http://localhost:5000";

export const registerUser = async (username) => {
  return axios.post(`${API_BASE_URL}/user/register`, { username });
};

export const acceptChallenge = async (inviteId, username) => {
  return axios.post(`${API_BASE_URL}/challenge/accept`, { invite_id: inviteId, username });
};
