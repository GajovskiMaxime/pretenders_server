from api.models import User, BlacklistToken


def verify_token_from_auth_header(auth_header):
    response_object = {
          'status': 'success'
    }, 200

    if not auth_header:
        response_object = {
            'status': 'fail',
            'message': 'Authorization header needed.'
        }, 401
        return response_object
    try:
        auth_token = auth_header.split(" ")[1]
    except IndexError:
        response_object = {
            'status': 'fail',
            'message': 'Bearer token malformed.'
        }, 401
        return response_object

    if not auth_token:
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }, 401
        return response_object

    user_id = User.decode_auth_token(auth_token)
    if not isinstance(user_id, int):
        response_object = {
            'status': 'fail',
            'message': 'Invalid token'
        }, 401
        return response_object
    else:
        response_object[0]['user_id'] = user_id

    if BlacklistToken.check_blacklist(auth_token):
        response_object = {
            'status': 'fail',
            'message': 'This token has expired.'
        }, 401

    return response_object
