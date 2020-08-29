from app import app, ma, db, api
from app.models import User, Department
from flask_restful import Resource
from flask import render_template
from flask import request
from flask import jsonify
from marshmallow import pre_dump, post_dump, pre_load, post_load, fields


# Index endpoint
@app.route("/")
def index():
	message = "Hello from flask_rest_api"
	return render_template('index.html', message=message)


class UserSchema(ma.Schema):
	"""Marshmallow output schema"""
	class Meta:
		fields = ("id", "username", "email", "_links")

	pages = fields.Integer(dump_to='numPages')
	per_page = fields.Integer(dump_to='perPage')
	total = fields.Integer(dump_to='totalItems')

	_links = ma.Hyperlinks({
		"self": ma.AbsoluteURLFor("users", id="<id>"),
		"collection": ma.AbsoluteURLFor("users"),
		"department": ma.AbsoluteURLFor("departments", id="<department_id>")
	})


class UserResource(Resource):
	"""API ressource for Users"""
	def get(self, id=None):
		if id:
			user = User.query.get_or_404(id)
			return user_schema.dump(user)
		else:
			offset = request.args.get('offset', 1, type=int)
			limit = request.args.get('limit', 10, type=int)
			users_query = User.query.paginate(offset, limit, False)
			total = users_query.total
			users_items = users_query.items
			data = dict()
			data["offset"] = offset
			data["limit"] = limit
			data["total"] = total
			data["data"] = users_schema.dump(users_items)
			return data

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
		if 'department_id' in request.json:
			department = Department.query.get(request.json["department_id"])
			if department:
				user.department_id = department.id
			else:
				user.department_id = None

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
		fields = ["name", "id", "_links"]

	_links = ma.Hyperlinks({
		"self": ma.AbsoluteURLFor("departments", id="<id>"),
		"users": ma.AbsoluteURLFor("department_users", id="<id>")
	})


class DepartmentResource(Resource):
	"""API ressource for a Departments"""
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


class UsersByDepartment(Resource):
	"""API ressource for all Users within Departments"""
	def get(self, id=None):
		if id:
			users = User.query.filter(User.department_id==id)
			return users_schema.dump(users)
		else:
			return None

user_schema = UserSchema()
users_schema = UserSchema(many=True)

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)



# Add endpoints
api.add_resource(UserResource, '/users', '/users/<int:id>', endpoint='users')
api.add_resource(DepartmentResource, '/departments', '/departments/<int:id>', endpoint='departments')
api.add_resource(UsersByDepartment, '/departments/<int:id>/users', endpoint='department_users')
