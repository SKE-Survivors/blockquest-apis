from tkinter import E
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from handler import DatabaseHandler, SessionHandler
from utils import build_response, encode_pwd

user_endpoint = Blueprint('user', __name__)
CORS(user_endpoint)

dbh = DatabaseHandler()
sh = SessionHandler()


@user_endpoint.route('/')
def index():
    return 'user ok!'


@user_endpoint.route("/profile", methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def user():
    email = request.args.get("email")
    if not email:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: email'}
        return build_response(status_code=400, body=body)

    user = dbh.find_user(email)
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
                "email": email,
                "username": username,
                "unlocked_lesson": lesson,
                "unlocked_story": story,
                "bag": bag
            }],
        }

    if request.method == "PUT":
        token = request.args.get("token")

        if not token:
            body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: token'}
            return build_response(status_code=400, body=body)

        data = request.json
        if not data:
            body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing body'}
            return build_response(status_code=400, body=body)

        if not sh.in_session(email, token):
            body = {"STATUS": "FAILED", "MESSAGE": f"Permission denied"}
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

        dbh.update_profile(email, **user.to_dict())
        body = {"STATUS": "SUCCESS", "MESSAGE": f"UPDATE USER {user.email}"}

    if request.method == "DELETE":
        token = request.args.get("token")

        if not token:
            body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: token'}
            return build_response(status_code=400, body=body)

        if not sh.in_session(email, token):
            body = {"STATUS": "FAILED", "MESSAGE": f"Permission denied"}
            return build_response(status_code=400, body=body)

        dbh.delete_user(user.email)
        body = {"STATUS": "SUCCESS", "MESSAGE": f"DELETE USER {user.email}"}

    return build_response(status_code=201, body=body)