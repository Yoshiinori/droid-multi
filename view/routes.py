from flask import Blueprint, render_template, session

view = Blueprint('view', __name__, template_folder='templates')

@view.route('/')
def index():
    username = 'hello'
    if 'username' in session:
      username = session['username']
    return render_template('index.html', username=username)
  
   

print('view working')