"""/seed_data/seed_sample_msgs.py"""

import sys
import os
from datetime import datetime, timedelta

from random import choice, randint

# Add the parent directory (chatfront) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from application import create_app
from extensions import db
from application.models import User, Message

from .sample_msgs import sample_messages

app = create_app()

with app.app_context():
    db.create_all()

    users = User.query.all()

    time_now = datetime.now()
    days_back = 50

    for i in range(1, 1001):
        user = choice(users)
        content = f"[msg #{i}] {choice(sample_messages)}"

        random_seconds = randint(0, days_back * 24 * 60 * 60)
        random_time = time_now - timedelta(seconds=random_seconds)
        
        message = Message(timestamp=random_time, content=content, sender_id=user.id)

        db.session.add(message)
        

    db.session.commit()

