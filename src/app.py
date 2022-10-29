from flask import Flask
from flask_cors import CORS
from decouple import config
import api

app = Flask(__name__)
CORS(app)

app.register_blueprint(api.auth_endpoint, url_prefix='/api/auth')
app.register_blueprint(api.google_endpoint, url_prefix='/api/auth/google')

app.register_blueprint(api.user_endpoint, url_prefix='/api/user')
app.register_blueprint(api.update_endpoint, url_prefix='/api/update')


@app.route('/')
def root():
    return 'all good!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config("APP_PORT"), debug=False)
