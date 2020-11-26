from flask import Flask
from auth.routes import auth
from view.routes import view
from user.routes import user
from score.routes import score
from matchmaking.routes import matchmaking
from room.routes import room
import os



app = Flask(__name__)

app.config["SECRET_KEY"] = "WTH BRO"
app.secret_key = 'hello'


app.register_blueprint(auth)
app.register_blueprint(view)
app.register_blueprint(user, url_prefix="/user/")
app.register_blueprint(score, url_prefix="/score/")
app.register_blueprint(matchmaking, url_prefix="/matchmaking/")
app.register_blueprint(room, url_prefix="/room/")



if os.environ['app'] == 'production':
  debug = True
  port = 8080
  host = '0.0.0.0'
else:
  debug = True
  port = 5000
  host = '127.0.0.1'

if __name__ == "__main__":
    app.run(debug=debug, port=port, host=host)



