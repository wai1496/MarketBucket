from flask import Blueprint, render_template, request, redirect, url_for, flash, escape, sessions
from flask_login import login_required, current_user
from market_bucket.images.forms import UploadForm, EditCaptionForm, DeleteForm
from market_bucket.helpers.helpers import allowed_file, upload_image
from werkzeug.utils import secure_filename
from market_bucket.images.model import Image, db
import random

images_blueprint = Blueprint('images',
                             __name__,
                             template_folder='templates')


@images_blueprint.route("<id>/new", methods=['GET'])
@login_required
def new(id):
    form = UploadForm()
    return render_template('images/upload.html', form=form)


@images_blueprint.route("<id>/upload", methods=['POST'])
@login_required
def upload(id):
    if int(id) == current_user.id:

        # check there is a file
        form = UploadForm()
        if "user_image" not in request.files:
            flash("No photo was uploaded!")
            return render_template('images/upload.html', form=form)

        # grab the photo and caption
        file = request.files["user_image"]
        caption = form.image_caption.data

        # check there is a name
        if file.filename == "":
            flash("Please give your photo a valid name!")
            return render_template('images/upload.html', form=form)

        # check file size
        if len(file.read()) > (2 * 1024 * 1024):
            flash("Please upload a file smaller than 2 MB!")
            return render_template('images/upload.html', form=form)

        # check correct extension and upload if valid
        if file and allowed_file(file.filename):
            file.seek(0)
            serial_filename = f'{current_user.id}.{random.randint(1,100000)}.{file.filename}'
            file.filename = secure_filename(serial_filename)
            upload_image(file)

            new_image = Image(
                user_id=id,
                image_name=str(file.filename),
                image_caption=caption
            )

            db.session.add(new_image)
            db.session.commit()
            flash('Product image added successfully!')
            # change redirect destination later
            return redirect(url_for('home', id=current_user.id))
        else:
            flash('Upload a valid image format!')
            return render_template('images/upload.html', form=form)

    return redirect(url_for('home', id=current_user.id))
