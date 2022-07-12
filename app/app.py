from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/')
@cross_origin()
def root():
    return 'all good!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)
