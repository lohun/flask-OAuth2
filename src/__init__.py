from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .flasklogin import login_manager
from .db import db
from src.routes import routes
from .utility import oauth

#app = Flask(__name__, static_folder="static")
app = Flask(__name__, static_folder="./templates/assets", static_url_path="/assets")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gooogle_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'routes.login'


def createApp():
    oauth.init_app(app)
    app.config["SECRET_KEY"] = "mysupersecretkey568"
    app.config['DEBUG'] = True
    app.register_blueprint(routes, url_prefix="/")

    return app