from models.base_model import BaseModel
import peewee as pw
from flask import url_for
from playhouse.hybrid import hybrid_property
from config import S3_LINK, S3_LOCATION
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
            return f"{S3_LOCATION}{self.user_image}"

    # TO DISPLAY AMOUNT IN HTML
    @hybrid_property
    def total_donations(self):
        from models.donation import Donation
        total = 0
        for donation in Donation.select().where(Donation.image_id == self.id):
            # where user_id == self.id TO SEE TOTAL DONATIONS A USER HAS RECEIVED
            total = total + donation.amount
        return round(total)
        # Donations: {{image.total_donations}}
