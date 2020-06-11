#!/usr/bin/env python3.6
import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_middleware import PrefixMiddleware
from config import Config
from loguru import logger

app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow()
api = Api(prefix='/api/v0')

class UserSchema(ma.Schema):
	"""Marshmallow output schema"""
	class Meta:
		fields = ("id", "username", "email", "_links")

	_links = ma.Hyperlinks({
		"uri": ma.URLFor("user", id="<id>"),
		"url": ma.AbsoluteURLFor("user", id="<id>")
	})

class UserResource(Resource):
	"""API ressource for a single user"""
	def get(self, id=None):
		if id:
			user = User.query.get_or_404(id)
			return user_schema.dump(user)
		else:
			users = User.query.all()
			return users_schema.dump(users)

	def post(self):
		user = User(
			username=request.json['username'],
			email=request.json['email']
		)
		db.session.add(user)
		db.session.commit()
		return user_schema.dump(user)

	def patch(self, id):
		user = User.query.get_or_404(id)
		print(request.json)

		if 'username' in request.json:
			user.username = request.json['username']
		if 'email' in request.json:
			user.email = request.json['email']

		db.session.commit()
		return user_schema.dump(user)

	def delete(self, id):
		user = User.query.get_or_404(id)
		db.session.delete(user)
		db.session.commit()
		return '', 204

# Specify which output schema to use for a single user
user_schema = UserSchema()

# Specify which output schema to use for a list of users
users_schema = UserSchema(many=True)

# Add endpoint for the User ressource
api.add_resource(UserResource, '/user', '/user/<int:id>', endpoint='user')

def create_app(config_class=Config):
	# app = Flask(__name__)
	app.config.from_object(config_class)

	# Set the prefix for serving the app. Uncomment if '/' shall be used
	app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/flask')

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
from app.models import User
