from api.models import User
from pretenders import db


def add_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user
