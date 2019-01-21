import logging

from flask import Flask
from flask_restful import Api, Resource

from tictactoe import settings
from tictactoe.api import Games, Game
from tictactoe import models
from tictactoe.database import db

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def create_app():
    app = Flask('tictactoe')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
    with app.app_context():
        db.init_app(app)
        db.create_all()

    rest_api = Api(app)

    rest_api.add_resource(Games, '/api/games')
    rest_api.add_resource(Game, '/api/games/<id>')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port='5000')
