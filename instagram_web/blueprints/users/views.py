from flask import Blueprint, render_template, request, flash, url_for, redirect
from models.user import User
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import re
from flask_login import login_user, logout_user, login_required, current_user
from helper import upload_file_to_s3
from config import S3_BUCKET

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
    if len(password) > 6 and re.search(r"[a-zA-Z]", password) and re.search(r"[\W]", password):
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email,
                    password=hashed_password)
        if user.save():
            flash(f"Welcome, {username}! :)")
            return redirect(url_for("users.new"))
        else:
            return render_template("users/new.html", errors=user.errors)
    else:
        flash(
            "Password invalid: must have 6 characters of upper, lowercase & special characters >:(")
        return redirect(url_for('users.new'))


# @users_blueprint.route('/<username>', methods=["GET"])
# @login_required
# def show(username):
#     user = User.get_or_none(User.username == username)

#     if current_user:


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    if not str(current_user.id) == id:
        flash("who you.")
    else:
        user = User.get_or_none(User.id == id)
        if not user:
            flash("no user found for id provided.")
        else:
            return render_template("users/edit.html", user=user)


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    # check if user exists
    if not str(current_user.id) == id:
        flash("who you.")
        return redirect(url_for("users.edit", id=id))
    else:
        user = User.get_or_none(User.id == current_user.id)
        updated_username = request.form.get("updated_username")
        updated_email = request.form.get("updated_email")

        user.username = updated_username
        user.email = updated_email

        if user.save():
            flash("profile updated :>")
            return redirect(url_for("users.edit", id=id))

        else:
            breakpoint()
            flash("oops you still the same")
            return redirect(url_for("users.edit", id=id))


@users_blueprint.route('/upload', methods=["POST"])
def upload():
    # user = User.get_or_none(User.id == current_user.id)
    if not 'profile_image' in request.files:
        flash('u no picha')
        return redirect(url_for('users.edit', id=current_user.id))
    file = request.files.get('profile_image')
    if file:
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, S3_BUCKET)
        # return str(output)

        upload_profile_img = User.update(
            profile_image=file.filename).where(User.id == current_user.id)

        if upload_profile_img.execute():
            flash("Successfully changed profile image!")
            return redirect(url_for("users.edit", id=current_user.id))
        else:
            flash("Some error occurred")
            return redirect(url_for("users.edit", id=current_user.id))

    else:
        return redirect(url_for('users.edit', id=current_user.id))
