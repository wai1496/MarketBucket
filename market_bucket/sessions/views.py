from omni_marketplace.users.model import User
from omni_marketplace.sessions.forms import LogInForm
from flask_login import login_user, current_user, login_required, logout_user
from flask import redirect, url_for, render_template, Blueprint, flash, request
from omni_marketplace import oauth, google, GOOGLE_REDIRECT_URI, db
import random

sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates')


@sessions_blueprint.route('/login', methods=['GET'])
def new():
    if current_user.is_authenticated:
        flash('You\'re already logged in!')
        return redirect(url_for('home'))  # change redirect destination later
    else:
        form = LogInForm()
        return render_template('sessions/sign_in.html', form=form)


@sessions_blueprint.route("/login", methods=['POST'])
def authenticate():
    form = LogInForm()
    user = User.query.filter_by(email=form.email.data.lower()).first()

    if user and user.check_password(form.password.data):
        login_user(user, remember=False)
        flash('Logged in successfully')
        next = request.args.get('next')
        # change redirect destination later
        return redirect(next or url_for('users.dashboard', id=current_user.id))

    else:
        flash('Wrong Email/Password')
        return render_template('sessions/sign_in.html', form=form)


@sessions_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('home'))


@sessions_blueprint.route('/check/google')
def google_authorize():
    redirect_uri = url_for(GOOGLE_REDIRECT_URI, _external=True)
    return google.authorize_redirect(redirect_uri)


@sessions_blueprint.route('/authorize/google')
def google_authorize_login():
    token = oauth.google.authorize_access_token()
    email = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user)
        flash('logged in successfully')
        return redirect(url_for('home'))  # change redirect destination later
    else:
        email = oauth.google.get(
            'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
        given_name = oauth.google.get(
            'https://www.googleapis.com/oauth2/v2/userinfo').json()['given_name']
        family_name = oauth.google.get(
            'https://www.googleapis.com/oauth2/v2/userinfo').json()['family_name']

        new_user = User(
            store_name=f'{given_name.lower()}{random.randint(1,1000)}',
            first_name=given_name,
            last_name=family_name,
            email=email.lower(),
            password=str(random.randint(10000000, 99999999))
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Omni-marketplace account created successfully!')
        flash('Please create a password for your Omni-marketplace account from the Settings tab')
        # send_signup_email(new_user.email)
        return redirect(url_for('home'))  # change redirect destination later
