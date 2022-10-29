import bcrypt
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from handler import DatabaseHandler, SessionHandler
from utils import build_response

auth_endpoint = Blueprint('auth', __name__)
CORS(auth_endpoint)

dbh = DatabaseHandler()
sh = SessionHandler()
salt = bcrypt.gensalt()


@auth_endpoint.route('/')
def index():
    return 'auth ok!'


@auth_endpoint.route("/signup", methods=["POST"])
@cross_origin()
def signup():
    try:
        data = request.json
        username = data["username"]
        email = data["email"]
        password = data["password"]
        confirm_password = data["confirm-password"]

    except Exception as err:
        return build_response(status_code=400, err=err)

    if not email:
        body = {"STATUS": "FAILED", "MESSAGE": f"Email is required!"}
        return build_response(status_code=400, body=body)
    if not password:
        body = {"STATUS": "FAILED", "MESSAGE": f"Password is required!"}
        return build_response(status_code=400, body=body)
    if confirm_password != password:
        body = {"STATUS": "FAILED", "MESSAGE": f"Confirm password is wrong!"}
        return build_response(status_code=400, body=body)

    # todo (option): check email format

    user = dbh.find_user(email)

    if user:
        body = {"STATUS": "FAILED", "MESSAGE": f"User already exist!"}
        return build_response(status_code=400, body=body)

    user = dbh.add_user(
        mail=email,
        username=username,
        password=bcrypt.hashpw(password.encode('utf-8'), salt),
    )

    token = sh.set_session(user.email)
    body = {
        "STATUS": "SUCCESS",
        "MESSAGE": {
            "email": user.email,
            "token": token
        }
    }
    return build_response(status_code=201, body=body)


@auth_endpoint.route("/login", methods=["POST"])
@cross_origin()
def login():
    try:
        data = request.json
        email = data["email"]
        password = data["password"]

    except Exception as err:
        return build_response(status_code=400, err=err)

    if not email:
        body = {"STATUS": "FAILED", "MESSAGE": f"Email is required!"}
        return build_response(status_code=400, body=body)
    if not password:
        body = {"STATUS": "FAILED", "MESSAGE": f"Password is required!"}
        return build_response(status_code=400, body=body)

    # check email and password
    user = dbh.find_user(email)
    if not user:
        body = {"STATUS": "FAILED", "MESSAGE": f"User does not exist!"}
        return build_response(status_code=400, body=body)
    if bcrypt.checkpw(password.encode('utf-8'), user.password) != password:
        body = {"STATUS": "FAILED", "MESSAGE": f"Wrong password!"}
        return build_response(status_code=400, body=body)

    # gen token and add to redis
    token = sh.set_session(user.email)
    body = {
        "STATUS": "SUCCESS",
        "MESSAGE": {
            "email": user.email,
            "token": token
        }
    }
    return build_response(status_code=201, body=body)


@auth_endpoint.route("/logout")
@cross_origin()
def logout():
    email = request.args.get("email")
    sh.remove_session(email)

    body = {"STATUS": "SUCCESS", "MESSAGE": f"Logout successfully"}
    return build_response(status_code=200, body=body)


@auth_endpoint.route("/check")
@cross_origin()
def check():
    email = request.args.get("email")
    token = request.args.get("token")

    msg = "User is authorized" if sh.check_session(
        email, token) else "User is not authorized"

    body = {"STATUS": "SUCCESS", "MESSAGE": msg}
    return build_response(status_code=200, body=body)