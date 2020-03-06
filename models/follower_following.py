import peewee as pw
from models.base_model import BaseModel
from models.user import User


class FollowerFollowing(BaseModel):
    fan = pw.ForeignKeyField(User, backref="idols")
    idol = pw.ForeignKeyField(User, backref="fans")

    def validate(self):
        print('No validate because me like danger')

    class Meta:
        indexes = ((('fan', 'idol'), True),)
