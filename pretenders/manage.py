import unittest

from flask.cli import FlaskGroup

from pretenders import create_app, db
from api.models import User
from api.models import BlacklistToken

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_database():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def seed_database():
    """Seeds the database."""
    db.session.add(User(username='michael', password="hermanmu@gmail.com"))
    db.session.add(User(username='michaelherman', password="michael@mherman.org"))
    db.session.commit()


if __name__ == '__main__':
    cli()
