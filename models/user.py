from models.base_model import BaseModel
import peewee as pw
import re
from flask_login import UserMixin
from flask import url_for
from playhouse.hybrid import hybrid_property, hybrid_method
from config import S3_LINK


class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)
    profile_image = pw.CharField(null=True, default=None)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)

        if duplicate_username and not duplicate_username.id == self.id:
            self.errors.append('username not unique boo')

        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_email and not duplicate_email.id == self.id:
            self.errors.append('e-mail not unique boo')

    @hybrid_property
    def profile_image_url(self):
        if self.profile_image:
            return f"{S3_LINK}/{self.profile_image}"
        else:
            return url_for("static", filename="pichas/default.jpg")

    @hybrid_method
    def is_following(self, user):
        from models.follower_following import FollowerFollowing
        return True if FollowerFollowing.get_or_none((FollowerFollowing.idol_id == user.id) & (FollowerFollowing.fan_id == self.id)) else False

    @hybrid_method
    def is_followed_by(self, user):
        from models.follower_following import FollowerFollowing
        return True if FollowerFollowing.get_or_none((FollowerFollowing.fan_id == user.id) & (FollowerFollowing.idol_id == self.id)) else False
