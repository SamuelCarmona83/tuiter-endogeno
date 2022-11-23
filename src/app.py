"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Tweet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response 😎"
    }

    return jsonify(response_body), 200

@app.route('/tweets', methods=['GET'])
def get_tweets():
    all_tweets = Tweet.query.all()
    return jsonify(
            [ tweet.serialize() for tweet in all_tweets ]
        ) , 200


@app.route('/tweets', methods=['POST'])
def post_tweet():
    body = request.json
    if "content" not in body:
        return "Ese tuit no tiene contenido! ⛔", 400
    else:
        new_tweet = Tweet(body["content"])
        db.session.add(new_tweet) #Memoria RAM
        try:
            db.session.commit() #Guarda en datos solidos!
            return "Tuit creado con exito! 🦄", 201
        except Exception as err:
            return "Ocurrio un error en el servidor 🐬", 500

        return jsonify(new_tweet.serialize()), 201
    return "Error algo ah ocurrido! 🐋", 404

















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
