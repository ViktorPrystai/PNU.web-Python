from app import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    developer = db.Column(db.String(100), nullable=True)
    genre = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.Float, nullable=True)

    def __init__(self, title, release_date, developer=None, genre=None, rating=None):
        self.title = title
        self.release_date = release_date
        self.developer = developer
        self.genre = genre
        self.rating = rating

