# CHATFRONT microservice

## codebase structure

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
