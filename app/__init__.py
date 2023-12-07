from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from  flask_login import LoginManager
app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


app.config.from_object('config')
db = SQLAlchemy(app)


migrate = Migrate(app, db)

from app import models
with app.app_context():
    db.create_all()
from app import views
