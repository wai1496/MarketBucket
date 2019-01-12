from market_bucket import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from market_bucket_api.blueprints.images.views import images_api_blueprint
from market_bucket_api.blueprints.users.views import users_api_blueprint
from market_bucket_api.blueprints.sessions.views import sessions_api_blueprint
from market_bucket_api.blueprints.marketplaces.views import marketplaces_api_blueprint
from market_bucket_api.blueprints.products.views import products_api_blueprint

app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1/')
app.register_blueprint(images_api_blueprint, url_prefix='/api/v1/images')
app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(marketplaces_api_blueprint, url_prefix='/api/v1/marketplaces')
app.register_blueprint(products_api_blueprint, url_prefix='/api/v1/products')
