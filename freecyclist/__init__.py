from flask import Flask
import json
from pprint import pprint

with open('secrets.json') as data_file:
    data = json.load(data_file)

app = Flask(__name__)

app.secret_key = 'development key'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'contact@example.com'
app.config["MAIL_PASSWORD"] = 'your-password'

from routes import mail
mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + data['username'] + ':' + data['password'] + '@localhost/freecyclist'

from models import db
db.init_app(app)

import freecyclist.routes
