from app import db
from flask_sqlalchemy import SQLAlchemy

class Department(db.Model):	
	"""SQLAlchemy model/description for our departments"""
	__tablename__ = 'department'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(), unique=True, nullable=False)
	users = db.relationship('User', backref='dep', lazy='dynamic')
	
	def __repr__(self):
		return '<Department %r>' % self.name	


class User(db.Model):
	"""SQLAlchemy model/description for our users"""
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(), unique=True, nullable=False)
	email = db.Column(db.String(), unique=True, nullable=False)
	department_id = db.Column(db.Integer, db.ForeignKey(Department.id))

	def __repr__(self):
		return '<User %r>' % self.username


