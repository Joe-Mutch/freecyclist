from freecyclist import app
from flask import render_template, request, flash, session, url_for, redirect
from forms import AlertForm, SignupForm, SigninForm
from flask_mail import Message, Mail
from models import db, User, Location, Alert, Keyword

mail = Mail()

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/alerts', methods=['GET', 'POST'])
def alerts():
  form = AlertForm()
  locations = Location.query.all()
  options = []
  for l in locations:
    options.append((l.id, l.name))

  form.location.choices = options

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('alerts.html', form=form)
    else:
      user = User.query.filter_by(email = session['email']).first()
      # return render_template('alerts.html', success=True)

      location = Location.query.filter_by(id=form.location.data).first()

      keywords = form.keywords.data.split(',')
      keyword_objs = []
      for keyword in keywords:
        keyword_obj = Keyword.query.filter_by(name=keyword).first()
        if not keyword_obj:
          keyword_obj = Keyword(name=keyword)
          db.session.add(keyword_obj)
          db.session.commit()
        keyword_objs.append(keyword_obj)

      alert = Alert(user=user, keywords=keyword_objs, locations=[location])
      db.session.add(alert)
      db.session.commit()

      return render_template('alerts.html', success=True)

  elif request.method == 'GET':
    return render_template('alerts.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  form.validate_on_submit()

  if 'email' in session:
    return redirect(url_for('profile'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      
      session['email'] = newuser.email
      return redirect(url_for('profile'))
  
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/profile')
def profile():

  if 'email' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(email = session['email']).first()

  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if 'email' in session:
    return redirect(url_for('profile')) 
      
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))
                
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():

  if 'email' not in session:
    return redirect(url_for('signin'))
    
  session.pop('email', None)
  return redirect(url_for('home'))
