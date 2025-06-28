import { useState, useEffect } from "react";

export default function useWebSocketStats() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:3001");

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === "statsUpdate") {
        setStats(message.payload);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
    };

    return () => {
      ws.close();
    };
  }, []);

  return stats;
}
