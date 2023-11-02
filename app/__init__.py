
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedbacks.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import views
from models import db