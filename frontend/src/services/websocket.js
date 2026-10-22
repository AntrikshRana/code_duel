export class BattleSocket {
  constructor(roomCode, onMessage, onStatusChange) {
    this.roomCode = roomCode;
    this.onMessage = onMessage;
    this.onStatusChange = onStatusChange;
    this.ws = null;
    this.connect();
  }

  connect() {
    let wsUrl;
    const backendUrl = import.meta.env.VITE_API_URL;
    if (backendUrl) {
      try {
        const url = new URL(backendUrl);
        const wsProtocol = url.protocol === 'https:' ? 'wss:' : 'ws:';
        wsUrl = `${wsProtocol}//${url.host}/ws/battle/${this.roomCode}/`;
      } catch (e) {
        wsUrl = `ws://localhost:8000/ws/battle/${this.roomCode}/`;
      }
    } else {
      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.hostname || 'localhost';
      wsUrl = `${wsProtocol}//${host}:8000/ws/battle/${this.roomCode}/`;
    }

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        if (this.onStatusChange) this.onStatusChange('connected');
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (this.onMessage) this.onMessage(data);
        } catch (e) {
          console.error("WS Parse error", e);
        }
      };

      this.ws.onclose = () => {
        if (this.onStatusChange) this.onStatusChange('disconnected');
      };

      this.ws.onerror = (err) => {
        console.error("WS Error:", err);
      };
    } catch (err) {
      console.error("Failed to connect websocket", err);
    }
  }

  send(action, payload = {}) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ action, payload }));
    }
  }

  close() {
    if (this.ws) {
      this.ws.close();
    }
  }
}
