from flask import jsonify, Blueprint, request, make_response
import simplejson as json
from market_bucket import User, Product, Marketplace, db, LAZADA_MARKET_KEY, LAZADA_MARKET_SECRET, SHOPEE_APP_ID, SHOPEE_APP_KEY
# from market_bucket.helpers.sendgrid import send_bid_email
from market_bucket.helpers.lazada_sdk.lazop.base import LazopClient, LazopRequest, LazopResponse
import time
import requests
import hmac
import hashlib
import xml.etree.ElementTree as ET


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
        laz_request2 = LazopRequest('/brands/get', 'GET')
        laz_request2.add_api_param('offset', '0')
        laz_request2.add_api_param('limit', '1000')
        response2 = client.execute(laz_request2)
        brands = response2.body['data']

        responseObject = {
            'status': 'success',
            'message': 'category tree returned',
            'tree': tree,
            'brands': brands
        }

        return make_response(jsonify(responseObject)), 200

    else:
        responseObject = {
            'status': 'failed',
            'message': 'Authentication failed'
        }

        return make_response(jsonify(responseObject)), 401


@products_api_blueprint.route('/lazada/attributes', methods=['GET'])
def lazada_category_attributes():
    client = LazopClient('https://api.lazada.com.my/rest',
                         LAZADA_MARKET_KEY, LAZADA_MARKET_SECRET)
    request = LazopRequest('/category/attributes/get', 'GET')
    request.add_api_param('primary_category_id', '6614')
    response = client.execute(request)
    return jsonify(response.body)


@products_api_blueprint.route('/lazada/new', methods=['POST'])
def lazada_new_product():
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
        post_data = request.get_json()
        access_token = Marketplace.query.filter_by(
            user_id=user_id, marketplace_name='lazada').first().access_token
        refresh_token = Marketplace.query.filter_by(
            user_id=user_id, marketplace_name='lazada').first().refresh_token
        payload = post_data.get('payload')
        category_id = post_data.get('id')
        name = post_data.get('name')
        description = post_data.get('description')
        color = post_data.get('color')
        brand = post_data.get('brand')
        price = post_data.get('price')
        quantity = post_data.get('quantity')
        content = post_data.get('package_content')
        height = post_data.get('package_height')
        weight = post_data.get('package_weight')
        width = post_data.get('package_width')
        length = post_data.get('package_length')
        client = LazopClient('https://api.lazada.com.my/rest',
                             LAZADA_MARKET_KEY, LAZADA_MARKET_SECRET)
        laz_request = LazopRequest('/product/create')
        laz_request.add_api_param('payload', f"<?xml version=\"1.0\" encoding=\"UTF-8\" ?> <Request>     <Product>         <PrimaryCategory>{category_id}</PrimaryCategory>         <SPUId></SPUId>         <AssociatedSku></AssociatedSku>         <Attributes>             <name>{name}</name>             <short_description>{description}</short_description>             <brand>{brand}</brand>             <model>no model</model>         </Attributes>         <Skus>             <Sku>                 <SellerSku>MarketBucket-{name}</SellerSku>                 <color_family>{color}</color_family>                 <images><image>https://steamcdn-a.akamaihd.net/steam/apps/470220/header.jpg?t=1507630376</image></images>                                  <quantity>{quantity}</quantity>                 <price>{price}</price>                 <package_length>{length}</package_length>                 <package_height>{height}</package_height>                 <package_weight>{weight}</package_weight>                 <package_width>{width}</package_width>                 <package_content>{content}</package_content>                 <tax_class>default</tax_class>                          </Sku>         </Skus>     </Product> </Request>")
        response = client.execute(laz_request, access_token)

        responseObject = {
            'status': 'success',
            'message': 'product added successfully',
        }
        breakpoint()
        return make_response(jsonify(responseObject)), 200

    else:
        responseObject = {
            'status': 'failed',
            'message': 'Authentication failed'
        }

        return make_response(jsonify(responseObject)), 401
