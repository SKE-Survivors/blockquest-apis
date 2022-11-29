from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from handler import DatabaseHandler, SessionHandler
from utils import build_response

update_endpoint = Blueprint('update', __name__)
CORS(update_endpoint)

dbh = DatabaseHandler()
sh = SessionHandler()


@update_endpoint.route('/')
def index():
    return 'update ok!'


@update_endpoint.route("/section/unlock", methods=["POST"])
@cross_origin()
def unlock_section():
    email = request.args.get("email")
    token = request.args.get("token")
    section_id = request.args.get("id")

    if not email:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: email'}
        return build_response(status_code=400, body=body)
    if not token:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: token'}
        return build_response(status_code=400, body=body)
    if not section_id:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: section_id'}
        return build_response(status_code=400, body=body)

    section = str(section_id).upper()

    if not sh.in_session(email, token):
        body = {"STATUS": "FAILED", "MESSAGE": f"Permission denied"}
        return build_response(status_code=400, body=body)

    user = dbh.find_user(email)

    l1 = list(user.unlocked_lesson.keys())
    l2 = list(user.unlocked_story.keys())
    if section not in l1 + l2:
        body = {
            "STATUS": "FAILED",
            "MESSAGE": f"Section does not exist (for this user)"
        }
        return build_response(status_code=400, body=body)

    dbh.unlock_section(email, section)
    body = {"STATUS": "SUCCESS", "MESSAGE": f"Section {section} unlocked"}
    return build_response(status_code=201, body=body)


@update_endpoint.route("/section/lock", methods=["POST"])
@cross_origin()
def lock_section():
    email = request.args.get("email")
    token = request.args.get("token")
    section_id = request.args.get("id")

    if not email:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: email'}
        return build_response(status_code=400, body=body)
    if not token:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: token'}
        return build_response(status_code=400, body=body)
    if not section_id:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: section_id'}
        return build_response(status_code=400, body=body)

    section = str(section_id).upper()

    if not sh.in_session(email, token):
        body = {"STATUS": "FAILED", "MESSAGE": f"Permission denied"}
        return build_response(status_code=400, body=body)

    user = dbh.find_user(email)

    l1 = list(user.unlocked_lesson.keys())
    l2 = list(user.unlocked_story.keys())
    if section not in l1 + l2:
        body = {
            "STATUS": "FAILED",
            "MESSAGE": f"Section does not exist (for this user)"
        }
        return build_response(status_code=400, body=body)

    dbh.unlock_section(email, section, False)
    body = {"STATUS": "SUCCESS", "MESSAGE": f"Section {section} locked"}
    return build_response(status_code=201, body=body)


@update_endpoint.route("/bag/add", methods=["POST"])
@cross_origin()
def add_item():
    email = request.args.get("email")
    token = request.args.get("token")
    item = request.args.get("item")

    if not email:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: email'}
        return build_response(status_code=400, body=body)
    if not token:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: token'}
        return build_response(status_code=400, body=body)
    if not item:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: item'}
        return build_response(status_code=400, body=body)

    if not sh.in_session(email, token):
        body = {"STATUS": "FAILED", "MESSAGE": f"Permission denied"}
        return build_response(status_code=400, body=body)

    dbh.update_bag(email, item)
    body = {"STATUS": "SUCCESS", "MESSAGE": f"{item} added"}
    return build_response(status_code=201, body=body)


@update_endpoint.route("/bag/remove", methods=["POST"])
@cross_origin()
def remove_item():
    email = request.args.get("email")
    token = request.args.get("token")
    item = request.args.get("item")

    if not email:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: email'}
        return build_response(status_code=400, body=body)
    if not token:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: token'}
        return build_response(status_code=400, body=body)
    if not item:
        body = {'STATUS': 'FAILED', 'MESSAGE': 'Missing argument: item'}
        return build_response(status_code=400, body=body)

    if not sh.in_session(email, token):
        body = {"STATUS": "FAILED", "MESSAGE": f"Permission denied"}
        return build_response(status_code=400, body=body)

    dbh.update_bag(email, item, False)
    body = {"STATUS": "SUCCESS", "MESSAGE": f"{item} removed"}
    return build_response(status_code=201, body=body)