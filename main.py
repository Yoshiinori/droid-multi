from flask import Flask
from auth.routes import auth
from view.routes import view

app = Flask(__name__)

app.config["SECRET_KEY"] = "WTH BRO"
app.secret_key = 'hello'


app.register_blueprint(auth, url_prefix="")
app.register_blueprint(view, url_prefix="")




if __name__ == "__main__":
  app.run(host="0.0.0.0", port="8080", debug=True)



