from flask import Blueprint, session, render_template, request, flash, url_for, redirect, abort
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user


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


@sessions_blueprint.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("logged out, byeeee")
    return redirect(url_for('home'))
