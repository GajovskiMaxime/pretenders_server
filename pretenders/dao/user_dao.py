from api.models import User
from pretenders import db


def add_user(username, password):
    try:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        response_object = {
          'status': 'success',
          'message': 'Successfully registered.'
        }, 201

    except Exception:
        response_object = {
          'status': 'fail',
          'message': 'Some error occurred. Please try again.'
        }, 401
    return response_object
