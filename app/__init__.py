#!/usr/bin/env python3.6
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_cors import CORS
from flask_middleware import PrefixMiddleware
from config import Config

app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow()
api = Api(prefix='/api/v0')

def create_app(config_class=Config):
	# app = Flask(__name__)
	app.config.from_object(config_class)

	# Set the prefix for serving the app. Uncomment if '/' shall be used
	app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/flask_rest_api')

	# Init database, create tables if needed
	db.init_app(app)
	with app.app_context():
		db.create_all()

	# Using Marshmallow for serialization/deserialization
	ma.init_app(app)

	# Create Api for this flask application using prefix
	api.init_app(app)

	return app

from app import models
from app import routes
