// /application/static/js/ws_client.js //

let socket = null;

function connectWebSocket(username) {
    // const WS_URL = "wss://144.24.142.130:443";
    // const WS_URL = "wss://oceanotech.in/chat"
    const WS_URL = "http://localhost:8000"
    socket = new WebSocket(WS_URL);
    
    socket.onopen = () => {
        console.log("✅ WebSocket connected");

        // Option - send userinfo
        const joinMsg = {
            type: "join",
            sender: username,
            room: "general"
        };
        socket.send(JSON.stringify(joinMsg));
    };

    socket.onmessage = (event) => {
        const data = event.data;
        console.log("📩 Message received:", data);

        appendMessageToUI(data);
    };

    socket.onclose = () => {
        console.warn("🔌 WebSocket disconnected")
    };

    socket.onerror = (err) => {
        console.error("X WebSocket error", err)
        // Optional: attempt reconnect or show user notification
    };

}

function sendMessage(text, username) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        const msg = {
            type: "chat",
            sender: username,
            room: "general",
            message: text
        };

        socket.send(JSON.stringify(msg));
    } else {
        console.error("Socket not open. Message not sent");
    }
}

function appendMessageToUI(messageText) {
    const chatBox = document.getElementById("chat-box");
    
    const msgDiv = document.createElement("div");
    msgDiv.className = "mb-2 p-2 bg-white border rounded";
    msgDiv.textContent = messageText;

    chatBox.insertBefore(msgDiv, chatBox.firstChild);
}

