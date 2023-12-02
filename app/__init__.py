from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
app = Flask(__name__)
bcrypt = Bcrypt(app)


app.config.from_object('config')
db = SQLAlchemy(app)


migrate = Migrate(app, db)

from app import models
with app.app_context():
    db.create_all()
from app import views
