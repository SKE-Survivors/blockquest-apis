from flask import Flask, Blueprint, url_for, request
from flask_cors import CORS, cross_origin
from authlib.integrations.flask_client import OAuth
from handler import DatabaseHandler, SessionHandler
from utils import build_response

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

google_endpoint = Blueprint('google-auth', __name__)
CORS(google_endpoint)

app = Flask(__name__)
CORS(app)

oauth = OAuth(app)
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)

dbh = DatabaseHandler()
sh = SessionHandler()


@google_endpoint.route('/')
def index():
    return 'google-auth ok!'


@google_endpoint.route("/login")
@cross_origin()
def google_login():
    redirect_uri = url_for("authorize", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@google_endpoint.route("/authorize")
@cross_origin()
def authorize():
    token = oauth.google.authorize_access_token()
    user = token['userinfo']

    try:
        data = request.json
        # check if user exist
        user = dbh.find_user(data["username"])
        # (if not) create user, add to database
        if not user:
            user = dbh.add_user(
                mail=data["mail"],
                username=data["username"],
                password=b"",  # or None
            )
    except Exception as err:
        body = {"STATUS": "FAILED", "MESSAGE": f"Authorization failed"}
        return build_response(status_code=400, err=err)

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