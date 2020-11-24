from flask import Blueprint, request, render_template, redirect, session, flash
import os
from pymongo import MongoClient
from datetime import timedelta
import env

auth = Blueprint('auth', __name__, template_folder='templates')

auth.permanent_session_lifetime = timedelta(days=1)

url = os.environ['url']
port = os.environ['port']

client = MongoClient(url, int(port))
db = client.droidmulti
collection = db.test

@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
  if 'username' in session:
    return redirect('/')
  else:
    if request.method == 'POST':
          req = request.form
          un = req['username']
          pd = req['password']
          username = str(un)
          password = str(pd)
          username_info = collection.find_one({'username': username})
          if (len(username) >= 3) and (len(password) >= 6):
            if username_info == None:
              post = {'username': username, 'password': password, 'ibancho_username': 'Not Verified', 'ibancho_id': 'Not Verified', 'recent_play': 'No plays yet', 'recent_score': 'No scores yet'}
              collection.insert_one(post)
              flash(f'Welcome to droid!multi Beta! {username}')
              return redirect('/login/')
            else:
              flash('Username Taken')
              return redirect('/signup/')
          else:
            flash('Insufficient Details')
            return redirect('/signup/')
    else:
      return render_template('signup.html')



@auth.route('/login/', methods=['GET', 'POST'])
def login():
  if 'username' in session:
    return redirect('/')
  else:
    if request.method == 'POST':
          req = request.form
          un = req['username']
          pd = req['password']
          username = str(un)
          password = str(pd)
          username_info = collection.find_one({'username': username})
          if (len(username) >= 3) and (len(password) >= 6):
            if (username_info != None) and (username_info['password'] == password):
              session.permanent = True
              session['username'] = username
              flash(f'Welcome to droid!multi Beta! {username}')
              return redirect(f'/user/{username}')
            else:
              flash('Wrong Credentials')
              return redirect('/login/')
          else:
            flash('Insufficient Details')
            return redirect('/login/')
    else:
      return render_template('login.html')


@auth.route('/logout/')
def logout():
  session.pop('username', None)
  return redirect('/')



print('auth working')

