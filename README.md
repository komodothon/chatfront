# ChatApp: Distributed Chat System

This is a distributed chat application developed and deployed on Oracle Cloud Infrastructure (OCI), comprising a Flask-based frontend, a WebSocket backend server, and a standalone PostgreSQL database.

Over the past three weeks, we have been building and live-streaming the development of this project on our [YouTube channel](https://www.youtube.com/watch?v=I__C33kdx5A&list=PL9Y1FPcAeZr21m8n7dkynGRS-qvOsg3Ld), covering real-time coding, architecture decisions, and deployments.

---

## 📐 System Architecture Overview
```
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
```


### 🔵 OCI VM #1 – Frontend + Auth + DB Access
- **NGINX Reverse Proxy**
  - Routes `/`, `/auth`, and static files
  - Terminates SSL (HTTPS)
- **chatfront (Flask App)**
  - Renders UI (HTML/JS)
  - Handles JWT-based user sessions
  - Communicates with:
    - `auth-service` for login/registration
    - `chatserv` (via WebSocket) for real-time messaging
    - PostgreSQL DB to store user and chat data
- **auth-service (Flask API)**
  - Manages user login/registration
  - Issues JWT tokens to authenticated clients
- **PostgreSQL (External, Standalone)**
  - Fully isolated, accessed only by `chatfront`

### CI/CD (GitHub Actions + Docker)
- Builds and pushes Docker image of `chatfront`
- SSH deploys directly to OCI VM #1
- Ensures smooth delivery of updates and patches

---

### 🟢 OCI VM #2 – WebSocket Backend
- **NGINX Reverse Proxy**
  - Routes `/ws` endpoint
  - SSL termination
- **chatserv (Fastapi WebSocket Server)**
  - Authenticates JWT from incoming WebSocket clients
  - Forwards messages to `chatfront` REST API for persistence
  - Tracks connected users in memory
  - Deployed as a `systemd` service for stability

---

## 🚀 Deployment Highlights
- Independently deployed services across two VMs
- Secure architecture with SSL termination and JWT-based auth
- Real-time updates using WebSockets
- GitHub Actions pipeline for automated CI/CD
- All progress openly documented via YouTube livestreams

---

Stay tuned to our [channel](https://www.youtube.com/@kadirtecs) for regular updates, dev logs, and live coding sessions as we continue improving this project!


## chatfront codebase structure

.
├── application
│   ├── forms
│   │   ├── __init__.py
│   │   └── loginform.py
│   ├── __init__.py
│   ├── models
│   │   ├── base.py
│   │   ├── __init__.py
│   │   ├── message.py
│   │   ├── room.py
│   │   └── user.py
│   ├── routes
│   │   ├── api
│   │   │   ├── chat.py
│   │   │   ├── __init__.py
│   │   │   ├── messages.py
│   │   │   └── presence.py
│   │   ├── auth.py
│   │   ├── __init__.py
│   │   └── main.py
│   ├── static
│   │   └── js
│   │       └── ws_client.js
│   ├── templates
│   │   ├── home.html
│   │   ├── layout.html
│   │   └── login.html
│   └── utils
│       ├── __init__.py
│       └── user_utils.py
├── arch.md
├── config.py
├── Dockerfile
├── extensions.py
├── instance
├── main
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 688ccedd3bb8_.py
│       └── 7ff9ebdaad0d_message_model_timestamp_column_timezone.py
├── README.md
├── requirements.txt
├── run.py
├── seed_data
│   ├── sample_msgs.py
│   ├── seed_sample_msgs.py
│   └── seed_sample_users.py
└── test1.py
