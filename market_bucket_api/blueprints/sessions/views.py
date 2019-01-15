from flask import jsonify, Blueprint, request, make_response, url_for
from market_bucket.users.model import User, db
from market_bucket import google, GOOGLE_REDIRECT_URI, oauth
from market_bucket.helpers.sendgrid import send_signup_email
import simplejson as json
import random

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
        lazada_token = None
        lazada_refresh = None
        shop_id = None
        for marketplace in user.marketplaces:
            if marketplace.marketplace_name == 'lazada':
                lazada_token = marketplace.access_token
                lazada_refresh = marketplace.refresh_token
            elif marketplace.marketplace_name == 'shopee':
                shop_id = marketplace.shop_id
        # del user.__dict__['_sa_instance_state']
        # del user.__dict__['password_hash']
        # del user.__dict__['marketplaces']
        # del user.__dict__['images']
        # del user.__dict__['products']

        responseObject = {
            'status': 'success',
            'message': 'Successfully signed in.',
            'auth_token': auth_token.decode(),
            # 'user': user.__dict__,
            'lazada_token': lazada_token,
            'lazada_refresh': lazada_refresh,
            'shop_id': shop_id
        }
        return make_response(jsonify(responseObject)), 200

    else:

        responseObject = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }

        return make_response(jsonify(responseObject)), 401


# @sessions_api_blueprint.route('/check/google', methods=['GET'])
# def google_authorize():
#     redirect_uri = url_for(GOOGLE_REDIRECT_URI, _external=True)
#     return google.authorize_redirect(redirect_uri)


@sessions_api_blueprint.route('/authorize/google', methods=['POST'])
def google_authorize_login():
    post_data = request.get_json()
    email = post_data.get('email')
    user = User.query.filter_by(email=email).first()

    if user:

        auth_token = user.encode_auth_token(user.id)
        lazada_token = None
        lazada_refresh = None
        shop_id = None
        for marketplace in user.marketplaces:
            if marketplace.marketplace_name == 'lazada':
                lazada_token = marketplace.access_token
                lazada_refresh = marketplace.refresh_token
            elif marketplace.marketplace_name == 'shopee':
                shop_id = marketplace.shop_id 
        # del user.__dict__['_sa_instance_state']
        # del user.__dict__['password_hash']
        # del user.__dict__['marketplaces']
        # del user.__dict__['images']
        # del user.__dict__['products']

        responseObject = {
            'status': 'success',
            'message': 'Successfully signed in.',
            'auth_token': auth_token.decode(),
            # 'user': user.__dict__,
            'lazada_token': lazada_token,
            'lazada_refresh': lazada_refresh,
            'shop_id': shop_id
        }

        return make_response(jsonify(responseObject)), 200

    else:
        first_name = post_data.get('first_name')
        last_name = post_data.get('last_name')

        new_user = User(
            store_name=f'{first_name.lower()}{random.randint(1,1000)}',
            first_name=first_name,
            last_name=last_name,
            email=email.lower(),
            password=str(random.randint(10000000, 99999999))
        )

        db.session.add(new_user)
        db.session.commit()
        send_signup_email(new_user.email, new_user.id)

        auth_token = new_user.encode_auth_token(new_user.id)
        # del new_user.__dict__['_sa_instance_state']
        # del new_user.__dict__['password_hash']
        # del new_user.__dict__['validation_errors']

        responseObject = {
            'status': 'success',
            'message': 'Successfully created a user and signed in.',
            'auth_token': auth_token.decode(),
            # 'user': new_user.__dict__
        }

        return make_response(jsonify(responseObject)), 201
