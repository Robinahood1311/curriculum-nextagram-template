from flask import Blueprint, jsonify
from models.user import User
from playhouse.shortcuts import model_to_dict

users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()
    user_data = []
    # model_to_dict converts user into DICTIONARY
    for user in users:
        model_to_dict(user)
        del user['password']
        # to delete password in dictionary
        user_data.append(user)

    return jsonify(user_data), 200
    # status code 200: this request is successful
    # returns json with all the user information
