from flask import Blueprint, request, render_template, redirect, session, flash
from pymongo import MongoClient
import os

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
    print(score + us)
    
    return 'success'
  else:
    return 'no dude stop'

        
