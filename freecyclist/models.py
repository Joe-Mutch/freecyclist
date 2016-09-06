from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from freecyclist import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
  # __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
  alert = db.relationship('Alert', backref='user', lazy='dynamic')

  def __init__(self, email, password):
    self.email = email.lower()
    self.set_password(password)

  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

locations = db.Table('locations',
    db.Column('location_id', db.Integer, db.ForeignKey('location.id')),
    db.Column('alert_id', db.Integer, db.ForeignKey('alert.id'))
)

class Alert(db.Model):
  # __tablename__ = 'alerts'
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  keywords = db.Column(db.Text)
  locations = db.relationship('Location', secondary=locations,
        backref=db.backref('alerts', lazy='dynamic'))

  def __init__(self, user, locations, keywords):
    self.user = user
    self.locations = locations
    self.keywords = keywords

class Location(db.Model):
  # __tablename__ = 'location'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(120))

  def __init__(self, name):
    self.name = name.lower()
