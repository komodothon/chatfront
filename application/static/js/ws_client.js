let socket = null;
let oldestTimestamp = null; // Track the timestamp of the oldest loaded message
let isLoading = false;
let users_online = new Set();


function logout() {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.close(1000, "User logged out");
  }
  console.log("socket closed.")
  window.location.href = "/auth/logout";
}



document.addEventListener("DOMContentLoaded", () => {
  loadChatHistory();
  connectWebSocket(CURRENT_USERNAME);

  const sendBtn = document.getElementById("send-btn");
  sendBtn.addEventListener("click", () => {
    const input = document.getElementById("message-input");
    const message = input.value.trim();
    if (message) {
      sendMessage(message, CURRENT_USERNAME);
      input.value = "";
    }
  });

  // Attach scroll event for infinite loading
  const chatContainer = document.getElementById("chat-container");
  chatContainer.addEventListener("scroll", handleInfiniteScroll);

  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", logout);
  }

});

function connectWebSocket(username) {
    // Production route
    // const WS_URL = `wss://chat.oceanotech.in/?token=${ws_token}`;

    // below for testing at self-PC
    // const WS_URL = `ws://localhost:8000/?token=${ws_token}`;

    // testing without token on fastapi ws listener
    const WS_URL = `ws://localhost:8000/ws/chat/?token=${ws_token}`;
  
    socket = new WebSocket(WS_URL);

    socket.onopen = () => {
        console.log("✅ WebSocket connected");

        const joinMsg = {
            type: "join",
            sender: username,
            room: "general"
        };
        socket.send(JSON.stringify(joinMsg));
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        let users_online = [];

        if (data.type === "chat") {
            console.log("📩 Message received:", data);
            renderSingleMessage(data, true);  // true = append to top
        };
        
        if (data.type === "presence") {
            console.log("📡 Online users at join:", data.users);
            replaceOnlineUserList(data.users);
        };

        if (data.type === "join") {
            console.log("👤 User joined:", data.sender);
            addUserOnline(data.sender);
        };

        if (data.type === "leave") {
            console.log("👋 User left:", data.sender);
            removeUserOnline(data.sender);
        };

    };

    socket.onclose = () => {
        console.warn("🔌 WebSocket disconnected");
    };

    socket.onerror = (err) => {
        console.error("❌ WebSocket error", err);
    };
}


function renderOnlineUsers() {
  const listEl = document.getElementById("online-users");
  listEl.innerHTML = ""; // Clear existing list

  Array.from(users_online).sort().forEach((username) => {
    const li = document.createElement("li");
    li.className = "list-group-item";
    li.textContent = username + (username === CURRENT_USERNAME ? " (You)" : "");
    listEl.appendChild(li);
  });
}

function addUserOnline(username) {
  users_online.add(username);
  renderOnlineUsers();
}

function removeUserOnline(username) {
  users_online.delete(username);
  renderOnlineUsers();
}

function replaceOnlineUserList(newList) {
  users_online = new Set(newList);
  renderOnlineUsers();
}


function sendMessage(text, username) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        const msg = {
            type: "chat",
            sender: username,
            room: "general",
            content: text,
        };
        socket.send(JSON.stringify(msg));
    } else {
        console.error("Socket not open. Message not sent");
    }
}

function renderSingleMessage(msg, toTop = false) {
    const chatBox = document.getElementById("chat-box");
    const msgDiv = document.createElement("div");
    msgDiv.className = "mb-2 p-2 border rounded";

    if (msg.sender === CURRENT_USERNAME) {
        msgDiv.classList.add("bg-primary", "text-white", "align-self-end");
    } else {
        msgDiv.classList.add("bg-secondary", "text-white", "align-self-start");
    }

    let formattedTime;

    if (msg.timestamp) {
        formattedTime = new Date(msg.timestamp).toLocaleString('en-GB', {
            weekday: 'short',
            day: '2-digit',
            month: 'short',
            year: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        });
    } else {
        // Use current time as a fallback
        formattedTime = new Date().toLocaleString('en-GB', {
            weekday: 'short',
            day: '2-digit',
            month: 'short',
            year: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        });
    }

    console.log("🕒 Display Time:", formattedTime);

    msgDiv.innerHTML = `
        <div><strong>${msg.sender}</strong></div>
        <div>${msg.content}</div>
        <div class="text-muted" style="font-size: 0.8em;">${formattedTime}</div>
    `;

    if (toTop) {
        chatBox.insertBefore(msgDiv, chatBox.firstChild);
    } else {
        chatBox.appendChild(msgDiv);
    }
}

async function loadChatHistory(before = null) {
    if (isLoading) return;
    isLoading = true;
    console.log(isLoading)

    try {
        let url = `/api/chat/chat_history?room=general&limit=50`;
        if (before) {
            const isoBefore = new Date(before).toISOString();
            url += `&before=${encodeURIComponent(isoBefore)}`;
        }

        const res = await fetch(url, {
            method: "GET",
            credentials: "include",
        });

        if (!res.ok) throw new Error("Failed to fetch chat history");

        const messages = await res.json();
        // console.log(messages);

        const chatBox = document.getElementById("chat-box");

        messages.forEach(msg => {
            renderSingleMessage(msg, false); // false = add to bottom
        });

        if (messages.length > 0) {
            oldestTimestamp = messages[messages.length - 1].timestamp;
            console.log("oldestTimestamp: ", oldestTimestamp)
        }

        if (!before) {


            // Initial load: scroll to top to see newest message
            const chatContainer = document.getElementById("chat-container");
            // console.log("chatContainer.scrollTop: ", chatContainer.scrollTop )
            // console.log("before:", before);

            chatContainer.scrollTop = 0;
            // console.log("chatContainer.scrollTop: ", chatContainer.scrollTop )

        }

    } catch (err) {
        console.error("💥 Error loading chat history:", err);
    } finally {
        isLoading = false;
    }
}

function handleInfiniteScroll() {
    const chatContainer = document.getElementById("chat-container");

    // When user nears the bottom (older messages side)
    const scrollPosition = chatContainer.scrollHeight - chatContainer.scrollTop - chatContainer.clientHeight;
    // console.log("scrollPosition: ", scrollPosition)

    if (scrollPosition < 50 && !isLoading && oldestTimestamp) {
        console.log("📜 Loading older messages before:", oldestTimestamp);
        loadChatHistory(oldestTimestamp);
    }
}
