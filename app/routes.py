from app import app, ma, db, api
from app.models import User, Department
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful_swagger import swagger
from flask import render_template, request
from marshmallow import fields


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
		"self": ma.AbsoluteURLFor("api.users", id="<id>"),
		"collection": ma.AbsoluteURLFor("api.users"),
		"department": ma.AbsoluteURLFor("api.departments", id="<department_id>")
	})


class UserResource(Resource):
	"""API ressource for Users"""

	@swagger.operation()
	def get(self, id=None):
		if id:
			user = User.query.get_or_404(id)
			data = dict()
			data["data"] = user_schema.dump(user)
			return data			
		else:
			parser = reqparse.RequestParser()
			parser.add_argument('offset', type=int, help='Offset value invalid', default=1)
			parser.add_argument('limit', type=int, help='Limit value invalid', default=10)
			args = parser.parse_args()

			query = User.query.paginate(args.offset, args.limit, False)
			total = query.total
			query_items = query.items
			data = dict()
			data["offset"] = args.offset
			data["limit"] = args.limit
			data["total"] = total
			data["data"] = users_schema.dump(query_items)
			return data

	@swagger.operation()
	def post(self):
		user = User(
			username=request.json["username"],
			email=request.json["email"]
		)
		db.session.add(user)
		db.session.commit()
		return user_schema.dump(user)

	@swagger.operation()
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

	@swagger.operation()
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
		"self": ma.AbsoluteURLFor("api.departments", id="<id>"),
		"users": ma.AbsoluteURLFor("api.department_users", id="<id>")
	})


class DepartmentResource(Resource):
	"""API ressource for Departments"""
	
	@swagger.operation()	
	def get(self, id=None):
		if id:
			department = Department.query.get_or_404(id)
			data = dict()
			data["data"] = department_schema.dump(department)
			return data						
		else:
			parser = reqparse.RequestParser()
			parser.add_argument('offset', type=int, help='Offset value invalid', default=1)
			parser.add_argument('limit', type=int, help='Limit value invalid', default=10)
			args = parser.parse_args()

			query = Department.query.paginate(args.offset, args.limit, False)
			total = query.total
			query_items = query.items
			data = dict()
			data["offset"] = args.offset
			data["limit"] = args.limit
			data["total"] = total
			data["data"] = departments_schema.dump(query_items)
			return data

	@swagger.operation()
	def post(self):
		department = Department(
			name=request.json["name"]
		)
		db.session.add(department)
		db.session.commit()
		return department_schema.dump(department)

	@swagger.operation()
	def patch(self, id):
		department = Department.query.get_or_404(id)

		if 'name' in request.json:
			department.name = request.json['name']

		db.session.commit()
		return department_schema.dump(department)

	@swagger.operation()
	def delete(self, id):
		department = Department.query.get_or_404(id)
		db.session.delete(department)
		db.session.commit()
		return '', 204


class UsersByDepartment(Resource):
	"""API ressource for Users within a Department"""
	def get(self, id=None):
		if id:
			parser = reqparse.RequestParser()
			parser.add_argument('offset', type=int, help='Offset value invalid', default=1)
			parser.add_argument('limit', type=int, help='Limit value invalid', default=10)
			args = parser.parse_args()

			query = User.query.filter(User.department_id==id).paginate(args.offset, args.limit, False)
			total = query.total
			query_items = query.items
			data = dict()
			data["offset"] = args.offset
			data["limit"] = args.limit
			data["total"] = total
			data["data"] = users_schema.dump(query_items)
			return data
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
