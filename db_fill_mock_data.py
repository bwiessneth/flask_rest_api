from app import app, create_app
from app import db
from app.models import User, Department
from flask_sqlalchemy import SQLAlchemy

app = create_app()

db.init_app(app)

with app.app_context():
	db.create_all()

	hr = Department(name='HR')
	sales = Department(name='Sales')
	legal = Department(name='Legal')
	engineering = Department(name='Engineering')
	db.session.add(hr)
	db.session.add(sales)
	db.session.add(legal)
	db.session.add(engineering)

	admin = User(username="admin", email="admin@example.com")
	guest = User(username="guest", email="guest@example.com")
	jan = User(username="jan", email="jan@example.com")
	hein = User(username="hein", email="hein@example.com")
	klaas = User(username="klaas", email="klaas@example.com")
	pit = User(username="pit", email="pit@example.com")

	db.session.add(admin)
	db.session.add(guest)
	db.session.add(jan)
	db.session.add(hein)
	db.session.add(klaas)
	db.session.add(pit)

	hr.users.append(admin)
	sales.users.append(jan)
	legal.users.append(hein)
	engineering.users.append(klaas)
	engineering.users.append(pit)

	db.session.commit()
