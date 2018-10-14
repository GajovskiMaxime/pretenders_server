
from flask import Blueprint, jsonify, request

from pretenders import db, create_app
from api.models import Contest

from dao.blacklist_tokens_dao import verify_token_from_auth_header

contests_blueprint = Blueprint('contests', __name__)


@contests_blueprint.route('/contests', methods=['GET'])
def contest_all():
    """Get all contests"""

    auth_header = request.headers.get('Authorization')
    resp, code = verify_token_from_auth_header(auth_header)
    if resp['status'] != 'success':
        return jsonify(resp), code

    response_object = {
        'status': 'success',
        'data': {
            'contests': [contest.serialize for contest in Contest.query.all()]
        }
    }
    return jsonify(response_object), 200


@contests_blueprint.route('/contests/<contest_id>', methods=['GET'])
def contest_single(contest_id):
    """Get single contest details"""

    auth_header = request.headers.get('Authorization')
    resp, code = verify_token_from_auth_header(auth_header)
    if resp['status'] != 'success':
        return jsonify(resp), code

    contest = Contest.query.filter_by(contest_id=contest_id).first()
    response_object = {
        'status': 'success',
        'data': contest.serialize
    }
    return jsonify(response_object), 200
