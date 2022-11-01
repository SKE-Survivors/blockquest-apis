from tkinter import E
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from handler import DatabaseHandler
from utils import build_response, encode_pwd

user_endpoint = Blueprint('user', __name__)
CORS(user_endpoint)

dbh = DatabaseHandler()

# todo: check login session (aka call /auth/check before)


@user_endpoint.route('/')
def index():
    return 'user ok!'


@user_endpoint.route("/profile", methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def user():
    mail = request.args.get("mail")
    if not mail:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument'}
        return build_response(status_code=400, body=body)

    user = dbh.find_user(mail)
    if not user:
        body = {"STATUS": "FAILED", "MESSAGE": f"User does not exist"}
        return build_response(status_code=400, body=body)

    if request.method == "GET":
        email = user.email
        username = user.username
        lesson = user.unlocked_lesson
        story = user.unlocked_story
        bag = user.bag
        body = {
            "STATUS":
            "SUCCESS",
            "userInfo": [{
                "mail": email,
                "username": username,
                "unlocked_lesson": lesson,
                "unlocked_story": story,
                "bag": bag
            }],
        }

    if request.method == "PUT":
        data = request.json
        if not data:
            body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing body'}
            return build_response(status_code=400, body=body)

        for field in data:
            # note: you can add more field to update here
            if field == "username":
                user.username = data[field]

            if field == "password":
                try:
                    confirm = data["confirm-password"]
                except Exception:
                    return build_response(
                        status_code=400,
                        body={
                            'STATUS': 'FAILED',
                            'MESSAGE': 'Missing confirm-password'
                        },
                    )
                if data[field] != confirm:
                    return build_response(
                        status_code=400,
                        body={
                            'STATUS': 'FAILED',
                            'MESSAGE': 'Confirm password mismatch'
                        },
                    )
                user.password = encode_pwd(data[field])

        dbh.update_profile(mail, **user.to_dict())
        body = {"STATUS": "SUCCESS", "MESSAGE": f"UPDATE USER {user.email}"}

    if request.method == "DELETE":
        dbh.delete_user(user.email)
        body = {"STATUS": "SUCCESS", "MESSAGE": f"DELETE USER {user.email}"}

    return build_response(status_code=201, body=body)