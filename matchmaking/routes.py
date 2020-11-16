from flask import Blueprint, request, render_template, redirect, session, flash
from ossapi import ossapi
import os
from pymongo import MongoClient
from tinydb import TinyDB, Query

mm = TinyDB('matchmaking.json')
search = Query()

api_key = os.environ["api_key"]
osu = ossapi(api_key)

url = os.environ['url']
port = os.environ['port']

client = MongoClient(url, int(port))
db = client.droidmulti
collection = db.test

matchmaking = Blueprint('matchmaking', __name__, template_folder='templates')

@matchmaking.route('/new/', methods=['GET', 'POST'])
def new():
  if 'username' in session:
    username = session['username']
    username_info = collection.find_one({'username': username})
    if username_info['ibancho_id'] != 'Not Verified':
      if request.method == 'POST':
        req = request.form
        beatmap_id = req['beatmap_id']
        getbm = osu.get_beatmaps({"s": beatmap_id})
        if not getbm:
          flash('Please enter a valid beatmap id.')
          return redirect('/matchmaking/new/')
        else:
          return render_template('selectmap.html', getbm=getbm, username=username)
      else:
        return render_template('selectmap.html')
    else:
      flash('Please verify your account')
      return redirect(f'/user/{username}')
  else:
    return redirect('/')
      

@matchmaking.route('/', methods=['POST', 'GET'])
def main_lobby():
  if request.method == 'GET':
    if 'username' in session:
      username = session['username']
      username_info = collection.find_one({'username': username})
      if username_info['ibancho_id'] != 'Not Verified':
        rooms = mm.all()
        return render_template('matchmaking.html', rooms=rooms)
      else:
        flash('Please verify your account')
        return redirect(f'/user/{username}')
    else:
      return redirect('/')
  else:
    req = request.json()
    map_name = req['map_name']
    map_id = req['map_id']
    difficulty_name = req['difficulty_name']
    stars = req['stars']
    bpm = req['bpm']
    player_host=  req['player_host']

