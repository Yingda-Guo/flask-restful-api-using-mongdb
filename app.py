#~movie-bag/app.py

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from database.db import initialize_db
from flask_restx import Api
from resources.errors import errors
from flask_mail import Mail
import os
from flask_mongoengine import MongoEngine

app = Flask(__name__)

# Add environmental variable
app.config.from_envvar('ENV_FILE_LOCATION')
mail = Mail(app)
authorizations = {
    'apikey': {
        'type' : 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(app, 
          errors=errors, 
          version='1.0', 
          title="Movie API Document", 
          description="API Document", 
          authorizations=authorizations)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'db': os.getenv('MONGODB_DATABASE'),
    'host': os.getenv('MONGODB_HOSTNAME'),
    'port': 27017,
    'username':os.getenv('MONGODB_USERNAME'),
    'password':os.getenv('MONGODB_PASSWORD')
}

# Start mongoDB
initialize_db(app)

from resources.routes import initialize_routes

# Start app from blueprint
initialize_routes(api)