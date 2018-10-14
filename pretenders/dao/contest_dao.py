import sys

from api.models import Contest
from pretenders import db


def add_contest(contest_arguments):
    try:

        contest = Contest(**contest_arguments)
        db.session.add(contest)
        db.session.commit()
        response_object = {
          'status': 'success',
          'message': 'Contest successfully created.',
          'data': contest.serialize
        }, 201

    except Exception:
        response_object = {
          'status': 'fail',
          'message': 'Some error occurred. Please try again.'
        }, 401
    return response_object
