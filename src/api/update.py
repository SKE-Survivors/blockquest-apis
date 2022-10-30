from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from handler import DatabaseHandler
from utils import build_response

update_endpoint = Blueprint('update', __name__)
CORS(update_endpoint)

dbh = DatabaseHandler()

# todo: check login session (aka call /auth/check before)


@update_endpoint.route('/')
def index():
    return 'update ok!'


@update_endpoint.route("/section/unlock", methods=["POST"])
@cross_origin()
def unlock_section():
    mail = request.args.get("mail")
    section_id = request.args.get("id")

    # todo: check args existence
    section = str(section_id).upper()

    user = dbh.find_user(mail)
    if not user:
        body = {"STATUS": "FAILED", "MESSAGE": f"User does not exist"}
        return build_response(status_code=400, body=body)

    l1 = list(user.unlocked_lesson.keys())
    l2 = list(user.unlocked_story.keys())
    if section not in l1 + l2:
        body = {
            "STATUS": "FAILED",
            "MESSAGE": f"Section not exist (for the user)"
        }
        return build_response(status_code=400, body=body)

    dbh.unlock_section(mail, section)
    body = {"STATUS": "SUCCESS", "MESSAGE": f"SECTION {section} UNLOCKED"}
    return build_response(status_code=201, body=body)


@update_endpoint.route("/section/lock", methods=["POST"])
@cross_origin()
def lock_section():
    mail = request.args.get("mail")
    section_id = request.args.get("id")

    # todo: check args existence
    section = str(section_id).upper()

    user = dbh.find_user(mail)
    if not user:
        body = {"STATUS": "FAILED", "MESSAGE": f"User does not exist"}
        return build_response(status_code=400, body=body)

    l1 = list(user.unlocked_lesson.keys())
    l2 = list(user.unlocked_story.keys())
    if section not in l1 + l2:
        body = {
            "STATUS": "FAILED",
            "MESSAGE": f"Section not exist (for the user)"
        }
        return build_response(status_code=400, body=body)

    dbh.unlock_section(mail, section, False)
    body = {"STATUS": "SUCCESS", "MESSAGE": f"SECTION {section} LOCKED"}
    return build_response(status_code=201, body=body)


@update_endpoint.route("/bag/add", methods=["POST"])
@cross_origin()
def add_item():
    mail = request.args.get("mail")
    item = request.args.get("item")

    # todo: check args existence

    if not dbh.find_user(mail):
        body = {"STATUS": "FAILED", "MESSAGE": f"User does not exist"}
        return build_response(status_code=400, body=body)

    dbh.update_bag(mail, item)
    body = {"STATUS": "SUCCESS", "MESSAGE": f"{item} ADDED"}
    return build_response(status_code=201, body=body)


@update_endpoint.route("/bag/remove", methods=["POST"])
@cross_origin()
def remove_item():
    mail = request.args.get("mail")
    item = request.args.get("item")

    # todo: check args existence

    if not dbh.find_user(mail):
        body = {"STATUS": "FAILED", "MESSAGE": f"User does not exist"}
        return build_response(status_code=400, body=body)

    dbh.update_bag(mail, item, False)
    body = {"STATUS": "SUCCESS", "MESSAGE": f"{item} REMOVED"}
    return build_response(status_code=201, body=body)