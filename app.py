#!/usr/bin/env python3.6
import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_cors import CORS
from loguru import logger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/flask_api.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app, prefix='/api/v0')
CORS(app)


class User(db.Model):
	"""SQLAlchemy model/descirption for User"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)

	def __repr__(self):
		return '<User %r>' % self.username


class UserSchema(ma.Schema):
	"""Marshmallow output schema"""
	class Meta:
		fields = ("id", "username", "email")


class UsersResource(Resource):
	"""API ressource for all users"""
	def get(self):
		users = User.query.all()
		return users_schema.dump(users)


class UserResource(Resource):
	"""API ressource for a single user"""
	def get(self, user_id=0):
		user = User.query.get_or_404(user_id)
		return user_schema.dump(user)

	def post(self):
		user = User(
			username=request.json['username'],
			email=request.json['email']
		)
		db.session.add(user)
		db.session.commit()
		return user_schema.dump(user)

	def patch(self, user_id):
		user = User.query.get_or_404(user_id)
		print(request.json)

		if 'username' in request.json:
			user.username = request.json['username']
		if 'email' in request.json:
			user.email = request.json['email']

		db.session.commit()
		return user_schema.dump(user)

	def delete(self, user_id):
		user = User.query.get_or_404(user_id)
		db.session.delete(user)
		db.session.commit()
		return '', 204


user_schema = UserSchema()
users_schema = UserSchema(many=True)
api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/user', '/user/<int:user_id>')


class PrefixMiddleware(object):
	"""
	Class to enable serving the app from a prefix
	"""

	def __init__(self, app, prefix=''):
		self.app = app
		self.prefix = prefix

	def __call__(self, environ, start_response):
		if environ['PATH_INFO'].startswith(self.prefix):
			environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
			environ['SCRIPT_NAME'] = self.prefix
			return self.app(environ, start_response)
		else:
			start_response('404', [('Content-Type', 'text/plain')])
			return ["This url does not belong to the app.".encode()]

# Set the prefix for serving the app. Uncomment if '/' shall be used
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/flask_api')

# index endpoint
@app.route("/")
def index():
	message = "Hello from flask_api"
	return render_template('index.html', message=message)

# If app.py is run directly start in debug mode
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=1025, debug=True)

