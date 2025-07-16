┌────────────────────────────┐      ┌────────────────────────────┐
│        Public Internet     │      │        Admin/You           │
│  (User on browser/phone)   │      │  (You deploy and manage)   │
└────────────┬───────────────┘      └────────────┬───────────────┘
             │                                   │
             ▼                                   ▼
  🌐 HTTPS Request                         ⚙️ SSH / GitHub Actions / Console
      to /login /chat
             │
             ▼
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       🔵 OCI VM #1                                         │
│                                 (Frontend + DB Server)                                     │
│   ┌────────────────────────────┐      ┌────────────────────────────────────┐               │
│   │   NGINX (Reverse Proxy)    │─────▶│      chatfront (Flask App)         │────────┐      │
│   │  - Routes / /auth /static  │      │  - Serves UI via HTML/JS           │        │      │
│   │  - SSL termination         │      │  - Talks to auth-service           │        │      │
│   └────────────────────────────┘      │  - Sends chat to WebSocket server  │        ▼      │
│                                       │  - Interacts with PostgreSQL       │  ┌───────────┐│
│                                       └────────────────────────────────────┘  │PostgreSQL ││
│                                          ▲     ▲                              │ Database  ││
│                                          │     │                              │(Standalone)│
│                                          │     └──────────────────────────────│ External  ││
│                                          │                                    │   Access  ││
│                     ┌────────────────────────────┐                            │    Only   ││
│                     │ auth-service (Flask API)   │                            │           ││
│                     │ - Handles user login/reg   │                            |           ││
│                     │ - Issues JWT to chatfront  │                            └───────────┘│ 
│                     └────────────────────────────┘                                         │
│    ⚙️ Docker + GitHub Actions for CI/CD:                                                   │
│       - Automates chatfront image build and push                                           │
│       - Deploys via SSH to VM #1                                                           │
└────────────────────────────────────────────────────────────────────────────────────────────┘
             │ JWT
             ▼
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       🟢 OCI VM #2                                         │
│                                (WebSocket Backend Server)                                  │
│                                                                                            │
│   ┌────────────────────────────┐     ┌────────────────────────────┐                        │
│   │   NGINX (Reverse Proxy)    │────▶│   chatserv (Python WS App) │                        │
│   │  - Routes /ws              │     │ - Handles WebSocket conn   │                        │
│   │  - SSL termination         │     │ - Verifies token from user │                        │
│   └────────────────────────────┘     │ - Calls chatfront to store │                        │
│                                      │   messages via REST API    │                        │
│                                      └────────────────────────────┘                        │
│                                                                 Manual Deployment:         │
│                                                                 - `chatserv` runs as a     │
│                                                                   systemd background       │
│                                                                   service on VM #2         │
└────────────────────────────────────────────────────────────────────────────────────────────┘
