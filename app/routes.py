from app import app, ma, db, api
from app.models import User
from flask_restful import Resource
from flask import render_template

# Index endpoint
@app.route("/")
def index():
	message = "Hello from flask_rest_api"
	return render_template('index.html', message=message)

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