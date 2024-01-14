from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app import db
from app.game.models import Game
from .schemas.game import GameSchema
from app.auth.api import required_token_restful

class GamesApi(Resource):
    def get(self):
        schema = GameSchema(many=True)
        games = Game.query.all()
        return {"games": schema.dump(games)}
    @required_token_restful
    def post(self):
        schema = GameSchema()
        data = request.get_json()

        try:
            game = schema.load(data)
            db.session.add(game)
            db.session.commit()
            return {"game": schema.dump(game)}, 201
        except ValidationError as e:
            return {"message": str(e)}, 400

class GameApi(Resource):

    @required_token_restful
    def get(self, id):
        schema = GameSchema()
        game = Game.query.get_or_404(id)
        return {"game": schema.dump(game)}

    @required_token_restful
    def put(self, id):
        schema = GameSchema()
        game = Game.query.get_or_404(id)
        data = request.get_json()

        try:
            game = schema.load(data, instance=game)
            db.session.commit()
            return {"game": schema.dump(game)}
        except ValidationError as e:
            return {"message": str(e)}, 400

    @required_token_restful
    def delete(self, id):
        game = Game.query.get_or_404(id)
        db.session.delete(game)
        db.session.commit()
        return {"message": f"Game with id {id} deleted"}


