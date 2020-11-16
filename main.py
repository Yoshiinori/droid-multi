from flask import Flask
from auth.routes import auth
from view.routes import view
from user.routes import user
from score.routes import score
from matchmaking.routes import matchmaking

app = Flask(__name__)

app.config["SECRET_KEY"] = "WTH BRO"
app.secret_key = 'hello'


app.register_blueprint(auth)
app.register_blueprint(view)
app.register_blueprint(user, url_prefix="/user/")
app.register_blueprint(score, url_prefix="/score/")
app.register_blueprint(matchmaking, url_prefix="/matchmaking/")




if __name__ == "__main__":
  app.run(host="0.0.0.0", port="8080", debug=True)



