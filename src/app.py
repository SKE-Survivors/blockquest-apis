from flask import Flask
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from loginpass import create_flask_blueprint, Google
from decouple import config
from handler import handle_authorize
import api

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)

oauth = OAuth(app)
services = [Google]  # add services here
oauth_endpoint = create_flask_blueprint(services, oauth, handle_authorize)

# /api/auth/login
app.register_blueprint(api.auth_endpoint, url_prefix='/api/auth')
# /api/auth/login/{service}
app.register_blueprint(oauth_endpoint, url_prefix='/api/auth/')

app.register_blueprint(api.user_endpoint, url_prefix='/api/user')
app.register_blueprint(api.update_endpoint, url_prefix='/api/update')


@app.route('/')
def root():
    return 'all good!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config("APP_PORT"), debug=False)
