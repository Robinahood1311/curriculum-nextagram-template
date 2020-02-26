from models.base_model import BaseModel
import peewee as pw
import re


class User(BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)

        if duplicate_username:
            self.errors.append('Username not unique boo')

        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_email:
            self.errors.append('Email not unique boo')

        weak_password = len(self.password) < 8

        if weak_password:
            self.errors.append('Password weak. >:(')


# def valid_password(string):
#     regex = r""
