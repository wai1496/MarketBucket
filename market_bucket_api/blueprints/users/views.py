from flask import jsonify, Blueprint, request, make_response
from market_bucket.users.model import User, db
from market_bucket.helpers.sendgrid import send_signup_email

users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.query.all()

    # there is probably a more efficient to do this
    users = [{"id": int(user.id), "store_name": user.store_name, "description": user.description,
              "email": user.email, "first_name": user.first_name, "last_name": user.last_name} for user in users]

    return jsonify(users)


@users_api_blueprint.route('/create', methods=['POST'])
def create():
    # get the post data
    post_data = request.get_json()

    new_user = User(
        store_name=post_data.get('store_name'),
        first_name=post_data.get('first_name'),
        last_name=post_data.get('last_name'),
        email=post_data.get('email').lower(),
        password=post_data.get('password')
    )

    if len(new_user.validation_errors) > 0:

        responseObject = {
            'status': 'failed',
            'message': new_user.validation_errors
        }

        return make_response(jsonify(responseObject)), 400

    else:
        db.session.add(new_user)
        db.session.commit()
        send_signup_email(new_user.email, new_user.id)
        auth_token = new_user.encode_auth_token(new_user.id)
        del new_user.__dict__['_sa_instance_state']
        del new_user.__dict__['password_hash']
        del new_user.__dict__['validation_errors']

        responseObject = {
            'status': 'success',
            'message': 'Successfully created a user and signed in.',
            'auth_token': auth_token.decode(),
            'user': new_user.__dict__
        }

        return make_response(jsonify(responseObject)), 201


@users_api_blueprint.route('/me', methods=['GET'])
def show():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        responseObject = {
            'status': 'failed',
            'message': 'No authorization header found'
        }

        return make_response(jsonify(responseObject)), 401

    user_id = User.decode_auth_token(auth_token)
    user = User.query.get(user_id)

    if user:
        del user.__dict__['_sa_instance_state']
        del user.__dict__['password_hash']
        return jsonify(user.__dict__)

    else:
        responseObject = {
            'status': 'failed',
            'message': 'Authentication failed'
        }

        return make_response(jsonify(responseObject)), 401


@users_api_blueprint.route('/update', methods=['PUT'])
def edit():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        responseObject = {
            'status': 'failed',
            'message': 'No authorization header found'
        }

        return make_response(jsonify(responseObject)), 401

    user_id = User.decode_auth_token(auth_token)
    editted_user = User.query.get(user_id)

    if editted_user:
        form = request.get_json()
        editted_user.first_name = form['first_name']
        editted_user.last_name = form['last_name']
        editted_user.email = form['email']
        editted_user.store_name = form['store_name']
        if form['password']:
            editted_user.set_password(form['password'])

        if len(editted_user.validation_errors) == 0:
            db.session.add(editted_user)
            db.session.commit()

            responseObject = {
                'status': 'success',
                'message': 'User details updated successfully'
            }
            return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'failed',
                'message': editted_user.validation_errors
            }
        return make_response(jsonify(responseObject)), 400

    else:
        responseObject = {
            'status': 'failed',
            'message': 'Authentication failed'
        }

        return make_response(jsonify(responseObject)), 401
