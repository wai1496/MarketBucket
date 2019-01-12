from flask import jsonify, Blueprint, request, make_response
from market_bucket.marketplaces.model import Marketplace
import simplejson as json

marketplaces_api_blueprint = Blueprint('marketplaces_api',
                                __name__,
                                template_folder='templates')


@marketplaces_api_blueprint.route('/', methods=['GET'])
def index():
    marketplaces = Marketplace.query.all()

    # all_billboards = []
    # for billboard in billboards:
    #     billboard.get_bid_times()
    #     del billboard.__dict__['bids']
    #     billboard.__dict__['bids'] = billboard.get_bids()
    #     del billboard.__dict__['_sa_instance_state']
    #     all_billboards.append(billboard.__dict__)

    responseObject = {
        'status': 'success',
        'message': 'All billboards returned',
        # 'all_billboards': all_billboards
    }

    return make_response(json.dumps(responseObject)), 200
