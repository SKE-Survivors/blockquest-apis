from flask import Blueprint
from flask_cors import cross_origin, request
from handler.database import DatabaseHandler
from utils import build_response

update_endpoint = Blueprint('update', __name__)
dbh = DatabaseHandler()


@update_endpoint.route("/section", methods=["POST"])
@cross_origin()
def unlock_section():
    mail = request.args.get("mail")
    section_id = request.args.get("id")

    dbh.unlock_section(mail, section_id)
    body = {"STATUS": "SUCCESS", "MESSAGE": f"SECTION {section_id} UNLOCKED"}

    return build_response(status_code=201, body=body)


@update_endpoint.route("/bag", methods=["POST"])
@cross_origin()
def update_bag():
    mail = request.args.get("mail")
    item = request.args.get("item")

    dbh.update_bag(mail, item)
    body = {"STATUS": "SUCCESS", "MESSAGE": f"{item} UPDATED"}

    return build_response(status_code=201, body=body)