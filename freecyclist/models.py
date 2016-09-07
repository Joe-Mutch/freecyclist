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

  def get_alerts(self):
    alerts = Alert.query.filter_by(user_id=self.id).all()
    return alerts

  def notify(self, result):
    print 'sending email'


locations = db.Table('locations',
    db.Column('location_id', db.Integer, db.ForeignKey('location.id')),
    db.Column('alert_id', db.Integer, db.ForeignKey('alert.id'))
)

keywords = db.Table('keywords',
    db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id')),
    db.Column('alert_id', db.Integer, db.ForeignKey('alert.id'))
)

class Result(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  alert_id = db.Column(db.Integer, db.ForeignKey('alert.id'))
  url = db.Column(db.String(300))
  title = db.Column(db.String(300))
  full_text = db.Column(db.Text)
  __table_args__ = (db.UniqueConstraint('alert_id', 'url', name='_alert_url_uc'),)

  def __init__(self, alert, url, title, full_text):
    self.alert = alert
    self.url = url
    self.title = title
    self.full_text = full_text

class Alert(db.Model):
  # __tablename__ = 'alerts'
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  keywords = db.relationship('Keyword', secondary=keywords,
        backref=db.backref('alerts', lazy='dynamic'))
  locations = db.relationship('Location', secondary=locations,
        backref=db.backref('alerts', lazy='dynamic'))
  result = db.relationship('Result', backref='alert', lazy='dynamic')

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

class Keyword(db.Model):
  # __tablename__ = 'location'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(120))

  def __init__(self, name):
    self.name = name.lower()
