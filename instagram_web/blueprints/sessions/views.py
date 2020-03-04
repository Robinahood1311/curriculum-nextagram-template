from flask import Blueprint, session, render_template, request, flash, url_for, redirect, abort
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from instagram_web.util.googleauth import oauth


sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/new', methods=["GET"])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=["POST"])
def login():
    username_to_check = request.form.get("username")
    password_to_check = request.form.get("password")

    user_exists = User.get_or_none(User.username == username_to_check)
    if user_exists:
        result = check_password_hash(user_exists.password, password_to_check)
        if result:
            login_user(user_exists)
            return redirect(url_for('home'))
        else:
            flash("incorrect password")
            return redirect(url_for('sessions.new'))
    else:
        flash("oops who you, sign up ples")
        return redirect(url_for('sessions.new'))


@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route("/authorize_google")
def authorize():
    token = oauth.google.authorize_access_token()

    if token:
        email = oauth.google.get(
            'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
        user = User.get_or_none(User.email == email)

    if not user:
        flash("oops who you, sign up ples")
        return redirect(url_for('sessions.new'))

    login_user(user)
    return redirect(url_for('home'))

    # else:
    #     flash("oops who you, sign up ples")
    #     return redirect(url_for('sessions.new'))


@sessions_blueprint.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("logged out, byeeee")
    return redirect(url_for('home'))
