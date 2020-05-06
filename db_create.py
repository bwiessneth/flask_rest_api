from app import db
from app import User

db.create_all()

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
db.session.commit()
