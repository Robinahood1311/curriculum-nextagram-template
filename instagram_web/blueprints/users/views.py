from flask import Blueprint, render_template, request, flash, url_for, redirect
from models.user import User
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
    if user.save():
        flash(f"Welcome, {username}! :)")
        return redirect(url_for("users.new"))
    else:
        return render_template("users/new.html", errors=user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
