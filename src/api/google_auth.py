from flask import Flask, Blueprint, url_for
from flask_cors import CORS, cross_origin
from authlib.integrations.flask_client import OAuth
from handler import DatabaseHandler
from utils import build_response
from decouple import config

google_endpoint = Blueprint('google-auth', __name__)
CORS(google_endpoint)

app = Flask(__name__)
CORS(app)

oauth = OAuth(app)
oauth.register(
    name="google",
    server_metadata_url=config("CONF_URL"),
    client_kwargs={"scope": "openid email profile"},
)
dbh = DatabaseHandler()


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
    # user["email"]
    # user["name"]

    # todo:
    # 1. check if user exist
    # 2. (if not) create user, add to database
    # 3. gen token and add to redis

    body = {"STATUS": "SUCCESS", "MESSAGE": f"Authorization successfully"}
    return build_response(status_code=201, body=body)