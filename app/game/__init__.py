from flask import Blueprint
from flask_restful import Api
from marshmallow import ValidationError
from .views import GamesApi, GameApi
from flask import jsonify

games_api_bp = Blueprint("games_api", __name__, url_prefix="/api")
api = Api(games_api_bp)

api.add_resource(GamesApi, "/games")
api.add_resource(GameApi, "/games/<int:id>")

@games_api_bp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400

