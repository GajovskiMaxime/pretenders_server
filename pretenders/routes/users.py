
from flask import Blueprint, jsonify, request

from api.models import User, BlacklistToken
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from dao.user_dao import add_user
from dao.blacklist_tokens_dao import verify_token_from_auth_header


from pretenders import db, create_app

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/auth/register', methods=['POST'])
def user_register():

    post_data = request.get_json()

    username = post_data.get('username')
    password = post_data.get('password')

    user = User.query.filter_by(username=username).first()

    if user:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return jsonify(response_object), 202

    resp, code = add_user(username, password)
    return jsonify(resp), code


@users_blueprint.route('/auth/login', methods=['POST'])
def user_login():
    post_data = request.get_json()
    try:
        username = post_data.get('username')
        password = post_data.get('password')
        user = User.query.filter_by(username=username).first()
        if not user:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return jsonify(response_object), 404

        if not Bcrypt(create_app()).check_password_hash(user.password, password):
            response_object = {
                'status': 'fail',
                'message': 'Wrong password.'
            }
            return jsonify(response_object), 401

        auth_token = User.encode_auth_token(user.user_id)
        if auth_token:
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token.decode()
            }
            return jsonify(response_object), 200

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Try again'
        }
        return jsonify(response_object), 500


@users_blueprint.route('/auth/status', methods=['GET'])
def user_status():
    auth_header = request.headers.get('Authorization')
    resp, code = verify_token_from_auth_header(auth_header)
    if resp['status'] != 'success':
        return jsonify(resp), code

    user = User.query.filter_by(user_id=resp['user_id']).first()
    response_object = {
        'status': 'success',
        'data': user.serialize
    }, 200
    return jsonify(response_object), 200


@users_blueprint.route('/auth/logout', methods=['POST'])
def user_logout():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        response_object = {
            'status': 'fail',
            'message': 'Authorization header needed.'
        }
        return jsonify(response_object), 401
    try:
        auth_token = auth_header.split(" ")[1]
    except IndexError:
        response_object = {
            'status': 'fail',
            'message': 'Bearer token malformed.'
        }
        return jsonify(response_object), 401

    if not auth_token:
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return jsonify(response_object), 401

    resp = User.decode_auth_token(auth_token)
    if not isinstance(resp, int):
        response_object = {
            'status': 'fail',
            'message': 'Invalid token'
        }
        return jsonify(response_object), 401

    blacklist_token = BlacklistToken(token=auth_token)
    try:
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return jsonify(response_object), 200

    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': e
        }
        return jsonify(response_object), 200
