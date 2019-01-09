import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_assets import Bundle, Environment
from authlib.flask.client import OAuth

import config

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# session options parameter is used to override session options. If provided it's a dict of parameters passed to the session's
db = SQLAlchemy(app, session_options={"autoflush": False})
# db = SQLAlchemy(app)

Migrate(app, db)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sessions.new"
login_manager.session_protection = "basic"
login_manager.login_message = "Please login to Omni-marketplace first"

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None


# google & lazada oauth setup
config = eval((os.environ['APP_SETTINGS']))
oauth = OAuth()
GOOGLE_REDIRECT_URI = os.environ['GOOGLE_REDIRECT_URI']
LAZADA_REDIRECT_URI = os.environ['LAZADA_REDIRECT_URI']

google = oauth.register('google',
                        client_id=config.GOOGLE_CLIENT_ID,
                        client_secret=config.GOOGLE_CLIENT_SECRET,
                        access_token_url='https://accounts.google.com/o/oauth2/token',
                        access_token_params=None,
                        refresh_token_url=None,
                        authorize_url='https://accounts.google.com/o/oauth2/auth',
                        api_base_url='https://www.googleapis.com/oauth2/v1/',
                        client_kwargs={
                            'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
                            'token_endpoint_auth_method': 'client_secret_basic',
                            'token_placement': 'header',
                            'prompt': 'consent'
                        }
                        )

lazada = oauth.register('lazada',
                        client_id=config.LAZADA_MARKET_KEY,
                        authorize_url='https://auth.lazada.com/oauth/authorize',
                        client_kwargs={
                            'scope': '',
                            'token_endpoint_auth_method': 'client_secret_basic',
                            'token_placement': 'header',
                            'prompt': 'consent'
                        }
                        )
#                       EXAMPLE_CLIENT_KWARGS = {
#     'signature_method': 'HMAC-SHA1',
#     'signature_type': 'HEADER',
#     'rsa_key': 'Your-RSA-Key'
# }

oauth.init_app(app)

# S3 initialisation and upload setup
S3_BUCKET = config.S3_BUCKET
S3_LOCATION = f'http://{S3_BUCKET}.s3.amazonaws.com/'
S3_KEY = config.S3_KEY
S3_SECRET = config.S3_SECRET

app.config['S3_BUCKET'] = S3_BUCKET
app.config['S3_KEY'] = S3_KEY
app.config['S3_SECRET'] = S3_SECRET

# Lazada app keys
LAZADA_TEST_KEY = config.LAZADA_TEST_KEY
LAZADA_TEST_SECRET = config.LAZADA_TEST_SECRET
LAZADA_MARKET_KEY = config.LAZADA_MARKET_KEY
LAZADA_MARKET_SECRET = config.LAZADA_MARKET_SECRET

# Home Page
@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template('home.html', id = current_user.id)
    else:
        return render_template('home.html')


# Grab the blueprints from the other views.py files for each "app"
# make sure route and method is defined in views.py
from market_bucket.users.views import users_blueprint
from market_bucket.sessions.views import sessions_blueprint
from market_bucket.images.views import images_blueprint
from market_bucket.marketplaces.views import marketplaces_blueprint
from market_bucket.products.views import products_blueprint

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix='/')
app.register_blueprint(images_blueprint, url_prefix='/images')
app.register_blueprint(marketplaces_blueprint, url_prefix='/marketplaces')
app.register_blueprint(products_blueprint, url_prefix='/products')


# Flask_Assets
assets = Environment(app)

js = Bundle('js/vendor/jquery_3.2.1.js', 'js/vendor/popper_1.11.0.js', 'js/vendor/bootstrap_4.1.1.js',
            filters='jsmin', output='gen/packed.%(version)s.js')

css = Bundle('css/vendor/bootstrap_4.1.1.css', 'css/style.css',
             filters='cssmin', output='gen/packed.%(version)s.css')

assets.register({'js_all': js, 'css_all': css})

# import user, image, product & marketplace models so that you can run migration
from market_bucket.users.model import User
from market_bucket.marketplaces.model import Marketplace
from market_bucket.images.model import Image
from market_bucket.products.model import Product
