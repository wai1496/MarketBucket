from flask import jsonify, Blueprint, request, make_response
import simplejson as json
from market_bucket import User, Product, Marketplace, db, LAZADA_MARKET_KEY, LAZADA_MARKET_SECRET, SHOPEE_APP_ID, SHOPEE_APP_KEY
# from market_bucket.helpers.sendgrid import send_bid_email
from market_bucket.helpers.lazada_sdk.lazop.base import LazopClient, LazopRequest, LazopResponse
import time
import requests
import hmac
import hashlib

products_api_blueprint = Blueprint('products_api',
                                   __name__,
                                   template_folder='templates')


@products_api_blueprint.route('/lazada', methods=['GET'])
def lazada_products():
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
        access_token = Marketplace.query.filter_by(
            user_id=user_id, marketplace_name='lazada').first().access_token
        refresh_token = Marketplace.query.filter_by(
            user_id=user_id, marketplace_name='lazada').first().refresh_token
        client = LazopClient('https://api.lazada.com.my/rest',
                             LAZADA_MARKET_KEY, LAZADA_MARKET_SECRET)
        laz_request = LazopRequest('/products/get', 'GET')
        laz_request.add_api_param('filter', 'live')
        laz_request.add_api_param('limit', '10')
        laz_request.add_api_param('options', '1')
        response = client.execute(laz_request, access_token)
        products = response.body['data']

        responseObject = {
            'status': 'success',
            'message': 'all products returned',
            'products': products
        }

        return make_response(jsonify(responseObject)), 200

    else:
        responseObject = {
            'status': 'failed',
            'message': 'Authentication failed'
        }

        return make_response(jsonify(responseObject)), 401


@products_api_blueprint.route('/shopee', methods=['GET'])
def shopee_products():
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
        shop_id = Marketplace.query.filter_by(
            user_id=user_id, marketplace_name='shopee').first().shop_id
        endpoint = "https://partner.shopeemobile.com/api/v1/items/get"
        request_body = json.dumps({'shopid': shop_id, 'partner_id': int(SHOPEE_APP_ID), 'timestamp': int(
            time.time()), 'pagination_offset': 0, 'pagination_entries_per_page': 100})
        signature = hmac.new(
            key=bytes(SHOPEE_APP_KEY, encoding="ascii"),
            msg=bytes(f'{endpoint}|{request_body}', encoding="ascii"),
            digestmod=hashlib.sha256).hexdigest()
        headers = {'Authorization': signature}
        response = requests.post(endpoint, headers=headers, data=request_body)

        products = []
        for item in response.json()['items']:
            item_id = item['item_id']
            endpoint = "https://partner.shopeemobile.com/api/v1/item/get"
            request_body = json.dumps({'shopid': shop_id, 'item_id': item_id, 'partner_id': int(SHOPEE_APP_ID), 'timestamp': int(
                time.time())})
            signature = hmac.new(
                key=bytes(SHOPEE_APP_KEY, encoding="ascii"),
                msg=bytes(f'{endpoint}|{request_body}', encoding="ascii"),
                digestmod=hashlib.sha256).hexdigest()
            headers = {'Authorization': signature}
            response = requests.post(
                endpoint, headers=headers, data=request_body)
            products.append(response.json()['item'])

        responseObject = {
            'status': 'success',
            'message': 'all products returned',
            'products': products
        }

        return make_response(jsonify(responseObject)), 200

    else:
        responseObject = {
            'status': 'failed',
            'message': 'Authentication failed'
        }

        return make_response(jsonify(responseObject)), 401


@products_api_blueprint.route('/lazada/tree', methods=['GET'])
def lazada_category_tree():
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
        access_token = Marketplace.query.filter_by(
            user_id=user_id, marketplace_name='lazada').first().access_token
        refresh_token = Marketplace.query.filter_by(
            user_id=user_id, marketplace_name='lazada').first().refresh_token
        client = LazopClient('https://api.lazada.com.my/rest',
                             LAZADA_MARKET_KEY, LAZADA_MARKET_SECRET)
        laz_request = LazopRequest('/category/tree/get', 'GET')
        response = client.execute(laz_request)
        tree = response.body['data']

        responseObject = {
            'status': 'success',
            'message': 'category tree returned',
            'tree': tree
        }

        return make_response(jsonify(responseObject)), 200

    else:
        responseObject = {
            'status': 'failed',
            'message': 'Authentication failed'
        }

        return make_response(jsonify(responseObject)), 401
