import bcrypt
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from handler import DatabaseHandler
from utils import build_response

user_endpoint = Blueprint('user', __name__)
CORS(user_endpoint)

dbh = DatabaseHandler()
salt = bcrypt.gensalt()


@user_endpoint.route('/')
def index():
    return 'user ok!'


# todo: choose btw line 13 and 14. if use line 14, remove else case (line 88) instead
# @user_endpoint.route("/", methods=["POST", "GET", "PUT", "DELETE"])
@user_endpoint.route("/")
@cross_origin()
def user():
    if request.method == "GET":
        try:
            mail = request.args.get("mail")
            user = dbh.find_user(mail=mail)

            email = user.email
            username = user.username
            password = user.password
            lesson = user.unlocked_lesson
            story = user.unlocked_story
            bag = user.bag

            body = {
                "STATUS":
                "SUCCESS",
                "userInfo": [{
                    "mail": email,
                    "username": username,
                    "password": password,
                    "unlocked_lesson": lesson,
                    "unlocked_story": story,
                    "bag": bag
                }],
            }

        except Exception as err:
            return build_response(status_code=400, err=err)

    # todo: remove this comment (after create register). POST will be in the register endpoint
    # elif request.method == 'POST':
    #     try:
    #         data = request.json
    #         user_handler.add_user(mail=data["mail"],
    #                               username=data["username"],
    #                               password=bcrypt.hashpw(
    #                                   data["password"].encode('utf-8'), salt))
    #         body = {"STATUS": "SUCCESS", "MESSAGE": f"ADD USER {data['mail']}"}
    #     except Exception as err:
    #         return build_response(status_code=400, err=err)

    elif request.method == "PUT":
        try:
            mail = request.args.get("mail")
            data = request.json

            for key in data:
                if key != "username" and key != "password":
                    return build_response(
                        {
                            'STATUS': 'FAILED',
                            'MESSAGE': 'INCORRECT BODY'
                        }, 400)
                if key == "password":
                    data[key] = bcrypt.hashpw(data[key].encode('utf-8'), salt)

            dbh.update_profile(mail, **data)
            body = {"STATUS": "SUCCESS", "MESSAGE": f"UPDATE USER {mail}"}

        except Exception as err:
            return build_response(status_code=400, err=err)

    elif request.method == "DELETE":
        try:
            mail = request.args.get("mail")

            dbh.delete_user(mail=mail)
            body = {"STATUS": "SUCCESS", "MESSAGE": f"DELETE USER {mail}"}

        except Exception as err:
            return build_response(status_code=400, err=err)

    else:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'INCORRECT METHOD'}
        return build_response(status_code=400, body=body)

    return build_response(status_code=201, body=body)