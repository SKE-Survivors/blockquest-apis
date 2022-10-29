from flask import Flask
from flask_cors import CORS, cross_origin
from decouple import config

from api.user import user_endpoint
from api.update import update_endpoint

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_endpoint, url_prefix='/api/user')
app.register_blueprint(update_endpoint, url_prefix='/api/update')


@app.route('/')
@cross_origin()
def root():
    return 'all good!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config("APP_PORT"), debug=False)
