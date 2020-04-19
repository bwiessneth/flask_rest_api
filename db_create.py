from app import db
db.create_all()	



from app import User

admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')

db.session.add(admin)
db.session.add(guest)
db.session.commit()
