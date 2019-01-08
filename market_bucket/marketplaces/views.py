from market_bucket.marketplaces.model import Marketplace, db
from flask import redirect, url_for, render_template, Blueprint, flash, request
from flask_login import current_user, login_required
from market_bucket.helpers.lazada_sdk.lazop.base import LazopClient, LazopRequest, LazopResponse
from market_bucket import LAZADA_TEST_KEY, LAZADA_TEST_SECRET, LAZADA_MARKET_KEY, LAZADA_MARKET_SECRET, LAZADA_REDIRECT_URI, lazada, oauth

marketplaces_blueprint = Blueprint(
    'marketplaces', __name__, template_folder='templates')


@marketplaces_blueprint.route('/check/lazada')
@login_required
def lazada_authorize():
    import pdb; pdb.set_trace()
    return lazada.authorize_redirect(LAZADA_REDIRECT_URI, _external=True)


@marketplaces_blueprint.route('/authorize/lazada')
def lazada_authorize_login():
    import pdb; pdb.set_trace()
    code = request.args.get('code')
    client = LazopClient("https://auth.lazada.com/rest",
                         LAZADA_MARKET_KEY, LAZADA_MARKET_SECRET)
    api_request = LazopRequest("/auth/token/create")
    api_request.add_api_param("code", code)
    response = client.execute(api_request)
    access_token = response.body.get('access_token')
    refresh_token = response.body.get('refresh_token')
    seller_id = response.body.get('country_user_info')[0].get('seller_id')
    short_code = response.body.get('country_user_info')[0].get('short_code')
    # email = response.body.get('account')
    print(response.body)

    new_marketplace = Marketplace(
        user_id=current_user.id,
        marketplace_name="lazada",
        shop_id=seller_id,
        shop_name=short_code,
        access_token=access_token,
        refresh_token=refresh_token
    )

    db.session.add(new_marketplace)
    db.session.commit()
    flash('Lazada has been added to your omni-marketplace!')
    return redirect(url_for('home'))  # change redirect destination later

# Not authorised yet :(


@marketplaces_blueprint.route('/check/<order>/lazada')
def check_order(order):
    client = LazopClient("https://api.lazada.com.my/rest",
                         LAZADA_MARKET_KEY, LAZADA_MARKET_SECRET)
    request = LazopRequest('/order/get', 'GET')
    request.add_api_param('order_id', str(order))
    response = client.execute(
        request, Marketplace.query.filter(
            Marketplace.user_id == current_user.id, Marketplace.marketplace_name == "lazada").first().access_token)
    print(response)
    print(response.type)
    print(response.body)
    import pdb
    pdb.set_trace()
    return redirect(url_for('home'))  # change redirect destination later
