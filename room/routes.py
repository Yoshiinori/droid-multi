from flask import Blueprint, request, render_template, redirect, session, flash
from ossapi import ossapi
import os
from pymongo import MongoClient
from tinydb import TinyDB, Query
from datetime import datetime
import env

rm = TinyDB('room.json')
find = Query()

url = os.environ['url']
port = os.environ['port']

uri = os.environ['mongo']
client = MongoClient(uri)
db = client.droidmulti
collection = db.test

room = Blueprint('room', __name__, template_folder='templates')

@room.route('/<id>/')
def room_lobby(id):
   room = rm.get(find.room_id == id)
   if 'username' in session:
      username = session['username']
      if room != None:
         if (username == room['player1'] or (username == room['player2'])):
            return render_template('room.html', room=room, username=username)
         else:
            return redirect('/matchmaking/')
      else:
         return redirect('/matchmaking/')
   else:
      return redirect('/')

@room.route('/stats/<id>/')
def stats(id):
   room = rm.get(find.room_id == id)
   user_stats_one = collection.find_one({'username': room['player1']})
   user_stats_two = collection.find_one({'username': room['player2']})
   try:
      user_one_song =  user_stats_one['recent_play_full'].split()[0]
      user_two_song =  user_stats_two['recent_play_full'].split()[0]
   except:
      user_one_song =  user_stats_one['recent_play_full']
      user_two_song =  user_stats_two['recent_play_full']
   try:
      user_one_version = user_stats_one['recent_play'].split()[-1]
      user_two_version = user_stats_two['recent_play'].split()[-1]
   except:
      user_one_version = user_stats_one['recent_play']
      user_two_version = user_stats_two['recent_play']
   print(user_two_song)
   if (user_one_song == room['map_id'])  and (user_two_song == room['map_id']) and (user_one_version == room['difficulty_name']) and (user_two_version == room['difficulty_name']):
      if user_stats_one['recent_score'] > user_stats_two['recent_score']:
         rm.update({'winner': room['player1']} ,find.room_id == id)
      elif user_stats_one['recent_score'] < user_stats_two['recent_score']:
         rm.update({'winner': room['player2']} ,find.room_id == id)
      elif user_stats_one['recent_score'] == user_stats_two['recent_score']:
         rm.update({'winner': 'tie'} ,find.room_id == id)
   return {
      'player1_stats': user_one_song,
      'player2_stats': user_two_song,
      'winner': room['winner']
   }

@room.route('/winner/<id>/')
def winner(id):
   room = rm.get(find.room_id == id)
   return render_template('winner.html', room=room)

@room.route('/exists/<id>')
def exists(id):
   room = rm.get(find.room_id == id)
   if room != None:
      return {
         'exist': 'yes'
      }
   else:
      return {
         'exist': 'no'
      }
