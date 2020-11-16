from flask import Blueprint, request, render_template, redirect, session, flash
from ossapi import ossapi
import os

api_key = os.environ["api_key"]
osu = ossapi(api_key)

matchmaking = Blueprint('matchmaking', __name__, template_folder='templates')

@matchmaking.route('/new/', methods=['GET', 'POST'])
def new():
  if request.method == 'POST':
    req = request.form
    beatmap_id = req['beatmap_id']
    getbm = osu.get_beatmaps({"s": beatmap_id})
    if not getbm:
      flash('Please enter a valid beatmap id.')
      return redirect('/matchmaking/new/')
    else:
      return render_template('selectmap.html', getbm=getbm)
  else:
    return render_template('selectmap.html')
   




