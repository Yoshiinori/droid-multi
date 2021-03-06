from flask import Blueprint, request, render_template, redirect, session, flash
from ossapi import ossapi
import os
from pymongo import MongoClient
from tinydb import TinyDB, Query
import random
import string
from datetime import datetime
import env
from discord_webhook import DiscordWebhook, DiscordEmbed


rm = TinyDB('room.json')
mm = TinyDB('matchmaking.json')
find = Query()

api_key = os.environ["api_key"]
osu = ossapi(api_key)

url = os.environ['url']
port = os.environ['port']

uri = os.environ['mongo']
client = MongoClient(uri)
db = client.droidmulti
collection = db.test

webhook = DiscordWebhook(url=os.environ['webhook'])

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
          flash('Please enter a valid beatmap id.', 'error')
          return redirect('/matchmaking/new/')
        else:
          flash(getbm, 'map')
          return redirect('/matchmaking/new/')
      else:
        return render_template('new.html', username=username)
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
    random_room = (''.join(random.choice(string.ascii_uppercase) for i in range(4)))
    req = request.form['data']
    map = req.split('QAWSEDZXC')
    map_name = map[0]
    map_id = map[1]
    difficulty_name = map[2]
    stars = map[3]
    bpm = map[4]
    player_host =  map[5]
    mm.insert({
      'map_name': map_name,
      'map_id': map_id,
      'difficulty_name': f'[{difficulty_name}].osu',
      'stars': stars,
      'bpm': bpm,
      'player1': player_host,
      'player2': None,
      'room_id': random_room,
      'winner': None
    })
    embed = DiscordEmbed(title=f'{player_host} Made a room!', description=f'**RoomID** {random_room}\n\nMap Name: {map_name}\nVersion: {difficulty_name}\nBPM: {bpm}', color=242424)
    webhook.add_embed(embed)
    response = webhook.execute()
    return redirect(f'/matchmaking/{random_room}')

@matchmaking.route('/<id>/')
def waiting_area(id):
  room = mm.get(find.room_id == id)
  if room != None:
    print(room)
    if 'username' in session:
      username = session['username']
      username_info = collection.find_one({'username': username})
      if username_info['ibancho_id'] != 'Not Verified':
        if username != room['player1']:
          rm.insert(room)
          rm.update({'player2': username}, find.room_id == id)
          mm.remove(find.room_id == id)
          return redirect(f'/room/{id}/')
        elif username == room['player1']:
           return render_template('waitingarea.html', id=id)
      else:
        flash('Please verify your account')
        return redirect(f'/user/{username}/')
    else:
      return redirect('/')
  else:
    flash('Invalid Room')
    return redirect('/matchmaking/')
 
  

