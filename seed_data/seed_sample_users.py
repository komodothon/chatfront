"""/seed_data/seed_sample_users.py"""

import sys
import os

# Add the parent directory (ch_auth) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from application import create_app
from extensions import db
from application.models import User

app = create_app()

with app.app_context():
    db.create_all()

    for i in range(1, 26):
        username = f"user{i}"
        email = f"user{i}@sample.com"
        first_name = f"First{i}"
        last_name = f"Last{i}"

        user = User(
            username=username, 
            email=email, 
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(plain_password=f"hello{i}")
        db.session.add(user)
        print(f"{user} added")
    
    db.session.commit()



        