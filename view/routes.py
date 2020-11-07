from flask import Blueprint, render_template

view = Blueprint('view', __name__, template_folder='templates')

@view.route('/')
def index():
    return render_template('index.html')

print('view working')