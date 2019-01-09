from flask import jsonify, Blueprint, request, make_response
from market_bucket.images.model import Image, db
from market_bucket.users.model import User
import random
from werkzeug.utils import secure_filename
from market_bucket.helpers.helpers import allowed_file, upload_image


images_api_blueprint = Blueprint('images_api',
                                __name__,
                                template_folder='templates')


@images_api_blueprint.route('/', methods=['GET'])
def index():
    if request.args.get('userId'):
        images = Image.query.with_entities(Image.image_url).filter_by(
            user_id=int(request.args['userId'])).all()
    else:
        images = Image.query.with_entities(Image.image_url).all()

    images = [image[0] for image in images]

    return jsonify(images)

# use this for products
# @images_api_blueprint.route('/me', methods=['GET'])
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
#         images = user.images
#         all_ads = []
#         for medium in media:
#             del medium.__dict__['_sa_instance_state']
#             all_ads.append(medium.__dict__)

#         responseObject = {
#             'status': 'success',
#             'message': 'All ads media for user returned',
#             'all_ads': all_ads
#         }

#         return make_response(jsonify(responseObject)), 201

#     else:
#         responseObject = {
#             'status': 'failed',
#             'message': 'Authentication failed'
#         }

#         return make_response(jsonify(responseObject)), 401


@images_api_blueprint.route("/upload", methods=['POST'])
def upload():
        # check there is a file, campaign_name and description
    form = request.form

    if "user_image" not in request.files:

        responseObject = {
            'status': 'fail',
            'message': "No image was uploaded!"
        }

        return make_response(jsonify(responseObject)), 401

    # grab the file and caption
    file = request.files["user_image"]
    user_id = form['user_id']
    product_id = form['product_id']
    caption = form['caption']

    # check there is a name
    if file.filename == "":

        responseObject = {
            'status': 'fail',
            'message': "Invalid file name"
        }

        return make_response(jsonify(responseObject)), 401

    # check file size
    if len(file.read()) > (10 * 1024 * 1024):

        responseObject = {
            'status': 'fail',
            'message': "Max size allowed is 20 MB"
        }

        return make_response(jsonify(responseObject)), 401

    # check correct extension and upload if valid
    if file and allowed_file(file.filename):
        file.seek(0)
        serial_filename = f'{user_id}.{product_id}.{random.randint(1,100000)}.{file.filename}'
        file.filename = secure_filename(serial_filename)
        upload_image(file)

        new_image = Image(
            user_id=id,
            product_id=product_id,
            image_name=str(file.filename),
            image_caption=caption
        )

        db.session.add(new_image)
        db.session.commit()

        # concepts = review_media(new_medium)
        # is_approved = new_medium.is_approved
        del new_image.__dict__['_sa_instance_state']

        responseObject = {
            'status': 'success',
            'message': 'Image uploaded successfully',
            'image': new_image.__dict__,
        }

        return make_response(jsonify(responseObject)), 201

    else:

        responseObject = {
            'status': 'fail',
            'message': "Image format not supported"
        }

        return make_response(jsonify(responseObject)), 401
