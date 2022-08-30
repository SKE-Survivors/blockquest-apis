from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from mongoengine import *
from decouple import config
import bcrypt

from model.user import UserHandler

app = Flask(__name__)
CORS(app)

user_handler = UserHandler()

salt = bcrypt.gensalt()

@app.route('/')
@cross_origin()
def root():
    return 'all good!'


def build_response(status_code, body=None, err=None):
    if err:
        return Response("{'STATUS':'FAILED, 'ERROR':'"+type(err).__name__+"'}", status=status_code, mimetype='application/json')
    else:
        return Response(str(body), status=status_code, mimetype='application/json')

@app.route("/user", methods=["POST", "GET", "PUT", "DELETE"])
@cross_origin()
def user():
    if request.method == 'POST':
        try:
            data = request.json
            user_handler.add_user(mail=data["mail"], username=data["username"], password=bcrypt.hashpw(data["password"].encode('utf-8'), salt))
            body = "{'STATUS':'ADD USER "+data['mail']+" SUCCESS'}"
        except Exception as err:
            return build_response(status_code=400, err=err)

    elif request.method == "GET":
        try:
            mail = request.args.get("mail")
            user = user_handler.find_user(mail=mail)
            
            email = user.email
            username = user.username
            password = user.password
            lesson = user.unlocked_lesson
            story = user.unlocked_story
            bag = user.bag

            body = { 
                    "STATUS": "GET USER SUCCESS", 
                    "userInfo": [
                        {
                            "mail": email,
                            "username": username,
                            "password": password,
                            "unlocked_lesson": lesson,
                            "unlocked_story": story,
                            "bag": bag
                        }
                        ],
                }
            
        except Exception as err:
            return build_response(status_code=400, err=err)
    
    elif request.method == "PUT":
        try:
            mail = request.args.get("mail")
            data = request.json

            for key in data:
                if key != "username" and key != "password":
                    return build_response("{'STATUS':'FAILED, INCORRECT BODY'", 400)
                if key == "password":
                    data[key] = bcrypt.hashpw(data[key].encode('utf-8'), salt)
            
            user_handler.update_profile(mail, **data)

            body="{'STATUS':'UPDATE USER "+mail+" SUCCESS'}"

        except Exception as err:
            return build_response(status_code=400, err=err)

    elif request.method == "DELETE":
        try:
            mail = request.args.get("mail")

            user_handler.delete_user(mail=mail)
            body = "{'STATUS': 'SUCCESS, DELETE "+mail+" '}"
        except Exception as err:
            return build_response(status_code=400, err=err)
    else:
        return build_response(status_code=400, body="{'STATUS':'FAILED, 'ERROR':'INCORRECT METHOD'}")

    return build_response(status_code=201, body=body)
        
@app.route("/update/section", methods=["POST"])
@cross_origin()
def unlock_section():
    mail = request.args.get("mail")
    section_id = request.args.get("id")
    user_handler.unlock_section(mail, section_id)
    return build_response(status_code=201, body="{'STATUS': 'SUCCESS, SECTION "+section_id+" UNLOCKED'}")

@app.route("/update/bag", methods=["POST"])
@cross_origin()
def update_bag():
    mail = request.args.get("mail")
    item = request.args.get("item")
    user_handler.update_bag(mail, item)
    return build_response(status_code=201, body="{'STATUS': 'SUCCESS, "+item+" UPDATED'}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config("APP_PORT"), debug=False)
