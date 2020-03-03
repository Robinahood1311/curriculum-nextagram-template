import peewee as pw
from models.base_model import BaseModel
from models.image import Image
from models.user import User


class Donation(BaseModel):
    # decimal field for currency or number
    amount = pw.DecimalField()
    # image.donation will give us the donations received for image
    image = pw.ForeignKeyField(Image, backref="donations")
    # user.donation will give us donations the user has made
    user = pw.ForeignKeyField(User, backref="donations")

    def validate(self):
        print('No validate because me like danger')
