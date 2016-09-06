from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from models import db, User

class AlertForm(Form):
  location = StringField("location",  [validators.DataRequired("Please enter a location.")])
  keywords = TextAreaField("keywords",  [validators.DataRequired("Please enter one or more keywords.")])
  submit = SubmitField("Send")

class SignupForm(Form):
  email = StringField("Email",  [validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.DataRequired("Please enter a password.")])
  submit = SubmitField("Create account")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False

    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True

class SigninForm(Form):
  email = StringField("Email",  [validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.DataRequired("Please enter a password.")])
  submit = SubmitField("Sign In")
  
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    user = User.query.filter_by(email = self.email.data).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False
