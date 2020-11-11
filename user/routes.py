from flask import Blueprint, render_template, redirect, session, flash, request
from pymongo import MongoClient
import os
from bs4 import BeautifulSoup
import requests

user = Blueprint('user', __name__, template_folder='templates')

url = os.environ['url']
port = os.environ['port']

client = MongoClient(url, int(port))
db = client.droidmulti
collection = db.test


@user.route('/<username>/')
def get_user(username):
    user_stats = collection.find_one({'username': username})
    verify = False
    if user_stats != None:
        if 'username' in session:
            user_in_session = session['username']
            if user_in_session == username:
                if user_stats['ibancho_id'] == 'Not Verified':
                    return render_template(
                        'user.html',
                        username=username,
                        user_stats=user_stats,
                        verify=True)
                else:
                    return render_template(
                        'user.html', username=username, user_stats=user_stats)
            else:
                return render_template(
                    'user.html', username=username, user_stats=user_stats)
        else:
            return render_template(
                'user.html', username=username, user_stats=user_stats)
    else:
        return 'no user found'


@user.route('/verify/')
def verify():
    if 'username' in session:
        username = session['username']
        user_stats = collection.find_one({'username': username})
        if user_stats['ibancho_id'] != 'Not Verified':
            return redirect(f'/user/{username}/')
        else:
            return render_template('verify.html', username=username)
    else:
        return redirect('/')


@user.route('/verify/<ibancho_id>/')
def verify_user(ibancho_id):
    if 'username' in session:
        username = session['username']
        user_stats = {'username': username}
        get_stats = collection.find_one({'ibancho_id': ibancho_id})
        if get_stats == None:
            try:
                get_user = requests.get(
                    f'http://ops.dgsrz.com/profile.php?uid={ibancho_id}')
                soup = BeautifulSoup(get_user.text, 'html.parser')
                ibancho_username = soup.find(class_='h3 m-t-xs m-b-xs').get_text()
                latest_map = soup.find(class_='list-group-item').find(
                    class_='block').get_text()
                if latest_map == 'Mykal Williams - Splatoon - Splattack (Remix) (foxybus) [Easy]':
                    data = {
                        '$set': {
                            'ibancho_id': ibancho_id,
                            'ibancho_username': ibancho_username
                        }
                    }
                    collection.update_one(user_stats, data)
                    return 'you are now verified'
                  
                else:
                    flash('Please play the correct map')
                    return redirect('/user/verify')
            except:
                flash('Wrong ID')
                return redirect('/user/verify/')
        else:
          flash('The id is taken')
          return redirect('/user/verify/')
    else:
      return redirect('/')

