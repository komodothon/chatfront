┌────────────────────────────┐      ┌────────────────────────────┐
│        Public Internet     │      │        Admin/You           │
│  (User on browser/phone)   │      │  (You deploy and manage)   │
└────────────┬───────────────┘      └────────────┬───────────────┘
             │                                    │
             ▼                                    ▼

  🌐 HTTPS Request                         ⚙️ SSH / SCP / OCI Console
      to /login /chat
             │
             ▼

┌────────────────────────────────────────────────────────────────────┐
│                          🔵 OCI VM #1                              │
│                        (Frontend Server)                           │
│                                                                    │
│   ┌────────────────────────────┐   ┌────────────────────────────┐  │
│   │   chatfront (Flask App)    │   │   auth-service (Flask API) │  │
│   │  - Serves UI via HTML/JS   │   │  - Handles user login/reg  │  │
│   │  - Sends login to /auth    │──▶│  - Validates + issues JWT  │  │
│   │  - Sends chat to WebSocket │   │                            │  │
│   └────────────────────────────┘   └────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
             │ JWT
             ▼

┌────────────────────────────────────────────────────────────────────┐
│                          🟢 OCI VM #2                              │
│                      (WebSocket Server)                            │
│                                                                    │
│   ┌────────────────────────────┐                                   │
│   │   chat_server_ws.py        │                                   │
│   │  - Handles socket.io chat  │                                   │
│   │  - Authenticates users     │◀── uses token to verify user      │
│   │  - Stores chat history     │                                   │
│   └────────────────────────────┘                                   │
└────────────────────────────────────────────────────────────────────┘
             │
             ▼

      📦 PostgreSQL Database (1 instance)
 ┌─────────────────────────────────────┐
 │        OCI Free VM / External DB    │
 │   - Stores users, credentials       │
 │   - Stores messages, timestamps     │
 │   - Used by auth + chat_server_ws   │
 └─────────────────────────────────────┘
