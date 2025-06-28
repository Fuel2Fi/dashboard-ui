const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const http = require("http");
const WebSocket = require("ws");

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

const statsPath = path.join(__dirname, "../public/stats.json");
const tradesPath = path.join(__dirname, "trades.json"); // Create this dummy file as needed

// GET current strategy stats
app.get("/api/stats", (req, res) => {
  fs.readFile(statsPath, "utf-8", (err, data) => {
    if (err) {
      console.error("Failed to read stats.json:", err);
      return res.status(500).json({ error: "Failed to read stats file." });
    }
    res.json(JSON.parse(data));
  });
});

// GET historical trades data
app.get("/api/trades", (req, res) => {
  fs.readFile(tradesPath, "utf-8", (err, data) => {
    if (err) {
      console.error("Failed to read trades.json:", err);
      return res.status(500).json({ error: "Failed to read trades file." });
    }
    res.json(JSON.parse(data));
  });
});

// POST update settings (example: toggle strategies)
app.post("/api/settings", (req, res) => {
  console.log("Received settings update:", req.body);
  res.status(200).json({ message: "Settings updated (stub)" });
});

// Create HTTP server & WebSocket server
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Broadcast function to all connected clients
function broadcast(data) {
  const msg = JSON.stringify(data);
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(msg);
    }
  });
}

// Periodically broadcast the current stats every 10 seconds
setInterval(() => {
  fs.readFile(statsPath, "utf-8", (err, data) => {
    if (!err) {
      try {
        const stats = JSON.parse(data);
        broadcast({ type: "statsUpdate", payload: stats });
      } catch (parseErr) {
        console.error("Failed to parse stats.json for broadcasting:", parseErr);
      }
    }
  });
}, 10000); // 10 seconds interval

// Start server with WebSocket support
server.listen(PORT, () => {
  console.log(`API & WebSocket server running on http://localhost:${PORT}`);
});

