from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from models.follower_following import FollowerFollowing
from models.user import User

follower_following_blueprint = Blueprint(
    'follower_following', __name__, template_folder="templates")


@follower_following_blueprint.route('/<idol_id>', methods=["GET", "POST"])
@login_required
def create(idol_id):
    idol = User.get_or_none(User.id == idol_id)
    follow = FollowerFollowing(fan_id=current_user.id, idol_id=idol.id)
    if follow.save():
        flash(f"you are now following {idol.username} :p")
        return redirect(url_for('users.show', username=idol.username))
    else:
        flash("oopsie, something no work D:")
        return redirect(url_for('users.show', username=idol.username))


# @follower_following_blueprint.route('/<idol_id>', methods=["POST"])
# @login_required
# def delete():
#     .delete_instance()
