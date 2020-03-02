from models.base_model import BaseModel
import peewee as pw
from flask import url_for
from playhouse.hybrid import hybrid_property
from config import S3_LINK
from models.user import User


class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref="images")
    user_image = pw.CharField(null=True, default=None)
    caption = pw.CharField(unique=False, null=False)

    def validate(self):
        print('No validate because me like danger')

    @hybrid_property
    def user_image_url(self):
        if self.user_image:
            return f"{S3_LINK}/{self.user_image}"
