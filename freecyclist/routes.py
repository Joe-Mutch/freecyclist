from freecyclist import app
from flask import render_template, request, flash, session, url_for, redirect
from forms import AlertForm, SignupForm, SigninForm
from flask_mail import Message, Mail
from models import db, User

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

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('alerts.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@example.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)

      return render_template('alerts.html', success=True)

  elif request.method == 'GET':
    return render_template('alerts.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  form.validate_on_submit()
  if 'email' in session:
    return redirect(url_for('profile')) 
  print 'Hit signup route'
  if request.method == 'POST':
    print 'is post'
    print request.form
    if form.validate() == False:
      print 'not valid'
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
