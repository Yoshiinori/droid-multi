from flask import Blueprint, request, render_template, redirect, session, flash
from pymongo import MongoClient
import os
import env

score = Blueprint('score', __name__)

url = os.environ['url']
port = os.environ['port']

client = MongoClient(url, int(port))
db = client.droidmulti
collection = db.test

@score.route('/', methods=['POST'])
def get_score():
  if request.host_url != "https://javadeserialize.yoshiinori.repl.co":
    req = request.form
    score = req['score']
    us = req['username']
    play = req['map']
    full_map = req['map_id']
    user_stats = {'ibancho_username': us}
    data = {
      '$set': {
        'recent_play': play,
        'recent_score': score,
        'recent_play_full': full_map
      } 
    }
    collection.update_one(user_stats, data)
    
    return 'success'
  else:
    return 'no dude stop'

        
