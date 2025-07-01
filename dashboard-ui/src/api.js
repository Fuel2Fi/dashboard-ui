import axios from "axios";

const API_BASE = "http://localhost:4000/api";

export async function getBalance() {
  const res = await axios.get(\`\${API_BASE}/balance\`);
  return res.data;
}

export async function getStrategy() {
  const res = await axios.get(\`\${API_BASE}/strategy\`);
  return res.data;
}

export async function getTrades() {
  const res = await axios.get(\`\${API_BASE}/trades\`);
  return res.data;
}
