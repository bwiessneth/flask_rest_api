from app import app, ma, db, api
from app.models import User, Department
from flask_restful import Resource
from flask import render_template
from flask import request

# Index endpoint
@app.route("/")
def index():
	message = "Hello from flask_rest_api"
	return render_template('index.html', message=message)



class UserSchema(ma.Schema):
	"""Marshmallow output schema"""
	class Meta:
		fields = ("id", "username", "email", "department_id", "_links")

	_links = ma.Hyperlinks({
		# "uri": ma.URLFor("user", id="<id>"),
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
			username=request.json["username"],
			email=request.json["email"]
		)
		db.session.add(user)
		db.session.commit()
		return user_schema.dump(user)

	def patch(self, id):
		user = User.query.get_or_404(id)

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

class DepartmentSchema(ma.Schema):
	"""Marshmallow output schema"""
	class Meta:
		fields = ["name", "id", "users", "_links"]

	users = ma.Nested(UserSchema, many=True)

	_links = ma.Hyperlinks({
		# "uri": ma.URLFor("department", id="<id>"),
		"url": ma.AbsoluteURLFor("department", id="<id>")
	})

class DepartmentResource(Resource):
	"""API ressource for a single user"""
	def get(self, id=None):
		if id:
			department = Department.query.get_or_404(id)
			return department_schema.dump(department)
		else:
			departments = Department.query.all()
			return departments_schema.dump(departments)

	def post(self):
		department = Department(
			name=request.json["name"]
		)
		db.session.add(department)
		db.session.commit()
		return department_schema.dump(department)

	def patch(self, id):
		department = Department.query.get_or_404(id)

		if 'name' in request.json:
			department.name = request.json['name']

		db.session.commit()
		return department_schema.dump(department)

	def delete(self, id):
		department = Department.query.get_or_404(id)
		db.session.delete(department)
		db.session.commit()
		return '', 204			



user_schema = UserSchema()
users_schema = UserSchema(many=True)

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)



# Add endpoints
api.add_resource(UserResource, '/user', '/user/<int:id>', endpoint='user')
api.add_resource(DepartmentResource, '/department', '/department/<int:id>', endpoint='department')