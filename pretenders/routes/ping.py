
from flask import Blueprint, jsonify


ping_blueprint = Blueprint('ping', __name__)


@ping_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })