from flask import Blueprint, request, render_template, redirect, session, flash
import pyrebase
import os
from pymongo import MongoClient

auth = Blueprint('auth', __name__, template_folder='templates')

config = {
    "apiKey": os.environ['apiKey'],
    "authDomain": os.environ['authDomain'],
    "databaseURL": os.environ['databaseURL'],
    "storageBucket": os.environ['storageBucket']
}

firebase = pyrebase.initialize_app(config)
fauth = firebase.auth()

url = os.environ['url']
port = os.environ['port']

client = MongoClient(url, int(port))
db = client.droidmulti
collection = db.test

@auth.route('/signup/')
def signup():
    return render_template('signup.html')

def new_acc(username, email):
  post = {'email': email, 'username': username}
  collection.insert_one(post)

@auth.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        req = request.form
        username = req['username']
        email = req['email']
        password = req['password']
        try:
            new_acc(username, email)
            fauth.create_user_with_email_and_password(email, password)
            return redirect('/account-created/')
            new_acc(username, email)
            
        except:
            flash('An eror occured, please try again.')
            return redirect('/signup/')

    return redirect("/")


@auth.route('/account-created/')
def account_created():
    return render_template('account-created.html')


@auth.route('/login/')
def login():
    return render_template('login.html')


@auth.route('/validate-account', methods=['GET', 'POST'])
def validate_account():
    if request.method == 'POST':
        req = request.form
        email = req['email']
        password = req['password']
        try:
            newacc = fauth.sign_in_with_email_and_password(email, password)
            newacc
            print(newacc)
            return redirect('/account-created/')
            
        except:
            flash('Wrong Credentials')
            return redirect('/login/')


print('auth working')

