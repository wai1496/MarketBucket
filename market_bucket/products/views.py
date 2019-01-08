from flask import redirect, url_for, render_template, Blueprint, flash, request
from flask_login import current_user, login_required
from market_bucket.helpers.lazada_sdk.lazop.base import LazopClient, LazopRequest, LazopResponse
from market_bucket import LAZADA_TEST_KEY, LAZADA_TEST_SECRET,LAZADA_MARKET_KEY,LAZADA_MARKET_SECRET, LAZADA_REDIRECT_URI, lazada, oauth


products_blueprint = Blueprint(
    'products', __name__, template_folder='templates')


@products_blueprint.route('<marketplace>/new')
def new_product(marketplace):
    client = LazopClient("https://api.lazada.com.my/rest",
                         LAZADA_MARKET_KEY, LAZADA_MARKET_SECRET)
    request = LazopRequest('/category/tree/get', 'GET')
    response = client.execute(request)
    print(response)
    print(response.type)
    print(response.body)
    import pdb
    pdb.set_trace()
    return render_template('products/new.html')
