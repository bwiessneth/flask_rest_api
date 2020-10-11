#!/usr/bin/env python3.6
import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_cors import CORS
from config import Config

app = Flask(__name__)
CORS(app)
db = SQLAlchemy()
ma = Marshmallow()

api_v0 = Blueprint("api", __name__)

api = swagger.docs(
	Api(api_v0),
	apiVersion="0.0",
	basePath="http://localhost:5000",
	resourcePath="/",
	produces=["application/json", "text/html"],
	api_spec_url="/spec",
	description="API v0 description",
)


def create_app(config_class=Config):
	# app = Flask(__name__)
	app.config.from_object(config_class)

	# Init database, create tables if needed
	db.init_app(app)
	with app.app_context():
		db.create_all()

	# Using Marshmallow for serialization/deserialization
	ma.init_app(app)

	# Create Api for this flask application using prefix
	api.init_app(app)

	app.register_blueprint(api_v0)
	return app


from app import models
from app import routes
