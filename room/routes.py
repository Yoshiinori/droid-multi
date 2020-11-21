from flask import Blueprint, request, render_template, redirect, session, flash
from ossapi import ossapi
import os
from pymongo import MongoClient
from tinydb import TinyDB, Query
from datetime import datetime

rm = TinyDB('room.json')
find = Query()

room = Blueprint('room', __name__, template_folder='templates')

@room.route('/<id>/')
def room_lobby(id):
   room = rm.get(find.room_id == id)
   if 'username' in session:
      username = session['username']
      if room != None:
         if (username == room['player1'] or (username == room['player2'])):
            return render_template('room.html')
         else:
            return redirect('/matchmaking/')
      else:
         return redirect('/matchmaking/')
   else:
      return redirect('/')

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