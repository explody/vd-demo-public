from config import app, db

from models import Person, Location, Company

with app.app_context():
    db.create_all()
