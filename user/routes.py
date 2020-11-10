from flask import Blueprint, render_template, redirect, session, flash
from pymongo import MongoClient
import os

user = Blueprint('user', __name__, template_folder='templates')

url = os.environ['url']
port = os.environ['port']

client = MongoClient(url, int(port))
db = client.droidmulti
collection = db.test


@user.route('/<username>')
def get_user(username):
    user_stats = collection.find_one({'username': username})
    if user_stats != None:
      if 'username' in session:
        return render_template(
            'user.html', username=username, user_stats=user_stats)
      else:
          return render_template(
            'user.html',username=username, user_stats=user_stats, edit='true')
    else:
        return 'no user found'
