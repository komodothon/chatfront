"""/application/utils/user_utils.py"""

from application.models import User

def get_user_from_id(id):
    user = User.query.get(id)

    return user
    