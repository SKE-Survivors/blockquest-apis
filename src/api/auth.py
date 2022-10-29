from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from handler import DatabaseHandler
from utils import build_response

auth_endpoint = Blueprint('auth', __name__)
CORS(auth_endpoint)

dbh = DatabaseHandler()


@auth_endpoint.route('/')
def index():
    return 'auth ok!'


@auth_endpoint.route("/login", methods=["POST"])
@cross_origin()
def login():
    email = request.form["email"]
    password = request.form["password"]

    if not email:
        body = {"STATUS": "FAILED", "MESSAGE": f"Email is required!"}
        return build_response(status_code=400, body=body)
    if not password:
        body = {"STATUS": "FAILED", "MESSAGE": f"Password is required!"}
        return build_response(status_code=400, body=body)

    # todo:
    # 1. check email and password
    # 2. gen token and add to redis

    body = {"STATUS": "SUCCESS", "MESSAGE": f"Login successfully"}
    return build_response(status_code=200, body=body)


@auth_endpoint.route("/logout")
@cross_origin()
def logout():
    # todo: remove token from redis (& refresh window)

    body = {"STATUS": "SUCCESS", "MESSAGE": f"Logout successfully"}
    return build_response(status_code=200, body=body)


# todo: add function to check token (return bool)