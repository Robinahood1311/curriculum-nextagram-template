from flask import Blueprint, render_template, request, flash, url_for, redirect
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import re
from flask_login import login_user, logout_user, login_required, current_user
from helper import upload_file_to_s3
from config import S3_BUCKET, S3_LOCATION
from models.image import Image

images_blueprint = Blueprint('images',
                             __name__,
                             template_folder='templates')


@images_blueprint.route('/', methods=["POST"])
@login_required
def create():
    # user = User.get_or_none(User.id == current_user.id)

    if not 'user_image' in request.files:
        flash('no picha provided')
        return redirect(url_for('users.show', username=current_user.username))

    user_image = request.files.get('user_image')
    caption = request.form.get('caption')

    if user_image:
        user_image.filename = secure_filename(user_image.filename)
        output = upload_file_to_s3(user_image, S3_BUCKET)

        if not output:
            flash("image cannot upload boo")
            return redirect(url_for('users.show', username=current_user.username))

        else:
            user_post = Image(user_id=current_user.id,
                              user_image=user_image.filename, caption=caption)

            if user_post.save():
                flash("new post added :3")
                return redirect(url_for('users.show', username=current_user.username))

            else:
                flash("oops that didn't work :<")
                return redirect(url_for('users.show', username=current_user.username))
    else:
        return redirect(url_for('users.show', username=current_user.username))
