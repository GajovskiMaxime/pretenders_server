import datetime

import jwt
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import func

from pretenders import db, create_app


class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    gender = db.Column(db.Boolean, default=True, nullable=True)
    birthdate = db.Column(db.DateTime, nullable=True)
    country = db.Column(db.String, nullable=True)
    about_me = db.Column(db.String, nullable=True)
    score = db.Column(db.Integer, default=0)
    nb_of_tokens = db.Column(db.Integer, default=20)
    registered_on = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = Bcrypt(create_app()).generate_password_hash(
            password, create_app().config['BCRYPT_LOG_ROUNDS']
        ).decode()

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                create_app().config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, create_app().config['SECRET_KEY'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @property
    def serialize(self):
        return {
            'user_id':          self.user_id,
            'username':         self.username,
            'gender':           self.gender,
            'birthdate':        self.birthdate,
            'country':          self.country,
            'about_me':         self.about_me,
            'score':            self.score,
            'nb_of_tokens':     self.nb_of_tokens,
            'registered_on':    self.registered_on
        }


class Contest(db.Model):

    __tablename__ = 'contest'

    contest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contest_type = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    close_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    nb_of_pretenders = db.Column(db.Integer, nullable=True)
    nb_of_pretenders_max = db.Column(db.Integer, nullable=False, default=20)
    nb_of_winners = db.Column(db.Integer, nullable=False, default=1)
    country = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, title, contest_type, country):
        self.title = title
        self.contest_type = contest_type
        self.country = country

    @property
    def serialize(self):
        return {
            'contest_id':           self.contest_id,
            'type':                 self.type,
            'created_at':           self.created_at,
            'close_date':           self.close_date,
            'end_date':             self.end_date,
            'nb_of_pretenders':     self.nb_of_pretenders,
            'nb_of_pretenders_max': self.nb_of_pretenders_max,
            'nb_of_winners':        self.nb_of_winners,
            'country':              self.country,
            'title':                self.title
        }


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String, unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
