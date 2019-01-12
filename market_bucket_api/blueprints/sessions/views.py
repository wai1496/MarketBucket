from flask import jsonify, Blueprint, request, make_response
from market_bucket.users.model import User

sessions_api_blueprint = Blueprint('sessions_api',
                                   __name__,
                                   template_folder='templates')


@sessions_api_blueprint.route('/login', methods=['POST'])
def sign_in():
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    user = User.query.filter_by(email=post_data.get('email')).first()

    if user and user.check_password(post_data.get('password')):
        auth_token = user.encode_auth_token(user.id)
        del user.__dict__['_sa_instance_state']
        del user.__dict__['password_hash']

        responseObject = {
            'status': 'success',
            'message': 'Successfully signed in.',
            'auth_token': auth_token.decode(),
            'user': user.__dict__
        }

        return make_response(jsonify(responseObject)), 201

    else:

        responseObject = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }

        return make_response(jsonify(responseObject)), 401
