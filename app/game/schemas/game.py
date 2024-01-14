from marshmallow import fields, validate
from app import ma
from app.game.models import Game

class GameSchema(ma.SQLAlchemyAutoSchema):
    title = fields.String(required=True, validate=[validate.Length(min=1, max=255)])
    release_date = fields.Date(required=True)
    developer = fields.String(validate=[validate.Length(max=100)])
    genre = fields.String(validate=[validate.Length(max=50)])
    rating = fields.Float(validate=validate.Range(min=0, max=10))

    class Meta:
        model = Game
        load_instance = True
