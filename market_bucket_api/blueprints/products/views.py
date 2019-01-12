from flask import jsonify, Blueprint, request, make_response
import simplejson as json
from market_bucket import User, Product, db
# from market_bucket.helpers.sendgrid import send_bid_email

products_api_blueprint = Blueprint('products_api',
                               __name__,
                               template_folder='templates')


# @products_api_blueprint.route('/', methods=['GET'])
# def index():
#     bids = Bid.query.all()
#     all_bids = []
#     for bid in bids:
#         del bid.__dict__['_sa_instance_state']
#         all_bids.append(bid.__dict__)

#     return json.dumps(all_bids)


# @products_api_blueprint.route('/new_bid', methods=['POST'])
# def new_bid():
#     # get the post data
#     post_data = request.get_json()
#     user_id = post_data.get('user_id')
#     amount = post_data.get('amount')
#     nonce_from_the_client = post_data.get('nonce')
#     result = gateway.transaction.sale({
#         "amount": amount,
#         "payment_method_nonce": nonce_from_the_client,
#         "options": {
#             "submit_for_settlement": False
#         }
#     })

#     if result.is_success:
#         new_bid = Bid(
#             user_id=user_id,
#             billboard_id=post_data.get('billboard_id'),
#             medium_id=post_data.get('medium_id'),
#             booking_at=post_data.get('booking_at'),
#             amount=amount
#         )
#         db.session.add(new_bid)
#         db.session.commit()
#         send_bid_email(User.query.get(user_id).email, new_bid.id)

#         responseObject = {
#             'status': 'success',
#             'message': result.transaction.status,
#             'details': f'{result.transaction.processor_response_code} : {result.transaction.processor_response_text}'
#         }

#         return make_response(jsonify(responseObject)), 201

#     else:
#         responseObject = {
#             'status': ' api success but payment failed',
#             'message': result.transaction.status,
#             'details': f'{result.transaction.processor_response_code} : {result.transaction.processor_response_text}'
#         }

#         return make_response(jsonify(responseObject)), 201


# @products_api_blueprint.route('/me', methods=['GET'])
# def show():
#     auth_header = request.headers.get('Authorization')

#     if auth_header:
#         auth_token = auth_header.split(" ")[1]
#     else:
#         responseObject = {
#             'status': 'failed',
#             'message': 'No authorization header found'
#         }

#         return make_response(jsonify(responseObject)), 401

#     user_id = User.decode_auth_token(auth_token)
#     user = User.query.get(user_id)

#     if user:
#         bids = user.bids
#         all_bids = []
#         for bid in bids:
#             del bid.__dict__['_sa_instance_state']
#             bid.__dict__['created_at_readable'] = bid.created_at_readable
#             bid.__dict__['booking_at_readable'] = bid.booking_at_readable
#             all_bids.append(bid.__dict__)

#         responseObject = {
#             'status': 'success',
#             'message': 'All bids for user returned',
#             'all_ads': all_bids
#         }

#         return make_response(json.dumps(responseObject)), 201

#     else:
#         responseObject = {
#             'status': 'failed',
#             'message': 'Authentication failed'
#         }

#         return make_response(jsonify(responseObject)), 401
