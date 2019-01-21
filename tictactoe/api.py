import random
import json

from flask_restful import Resource, reqparse

from tictactoe import models
from tictactoe.database import db


class Games(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('player1', required=True, type=str, help='Player one')
    parser.add_argument('player2', required=True, type=str, help='Player two')

    def get(self):
        return [game.dictify() for game in models.Games.query.all()]

    def post(self):
        args = self.parser.parse_args()
        circle, cross = random.sample([args['player1'], args['player2']], 2)
        new_game = models.Games(
            circle=circle,
            cross=cross,
            board=models.EMPTY_BOARD,
            next_turn=random.choice(['circle', 'cross']),
        )
        db.session.add(new_game)
        db.session.commit()
        return new_game.dictify()

class Game(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('player', type=str, required=True, help='Player')
    parser.add_argument('x', type=int, required=True, help='X coordinate of space')
    parser.add_argument('y', type=int, required=True, help='Y coordinate of space')

    def get(self, id):
        game = models.Games.query.get_or_404(id)
        return game.dictify()

    def post(self, id):
        game = models.Games.query.get_or_404(id)
        args = self.parser.parse_args()
        x = args['x']
        y = args['y']

        if game.closed:
            return 'Game is over', 400
        current_player_name = getattr(game, game.next_turn)

        if current_player_name != args['player']:
            return "Invalid player. It's {}'s turn.".format(current_player_name), 400

        if x < 0 or x >= len(game.board[0]) or y < 0 or y >= len(game.board):
            return "Invalid Space", 400

        if game.board[x][y] != models.EMPTY:
            return "Space already taken", 400

        board = game.board
        board[x][y] = getattr(models, game.next_turn.upper())

        stmt = db.update(models.Games).where(
            models.Games.id==id
        ).values(
            board=board

        )
        db.engine.execute(stmt)

        closed, winner = self.game_state(board)
        if closed:
            game.closed = True
            game.winner = winner
        else:
            game.next_turn = 'circle' if game.next_turn == 'cross' else 'cross'

        db.session.commit()

        return game.dictify()

    def game_state(self, board):
        """
            Returns the game state and the winner if any
        """
        columns = [set(), set(), set()]
        diagnol1 = set()

        for y, row in enumerate(board):
            row_set = set(row)
            if len(row_set) == 1 and -1 not in row_set:
                return True, models.BOARD_LOOKUP[row_set.pop()]['long']
            for x, space in enumerate(row):
                columns[x].add(space)
                if x == y:
                    diagnol1.add(space)
        cols = [foo for foo in columns if len(foo) == 1 and -1 not in foo]
        if cols:
            return True, models.BOARD_LOOKUP[cols[0].pop()]['long']

        if len(diagnol1) == 1 and -1 not in diagnol1:
            return True, models.BOARD_LOOKUP[diagnol1.pop()]['long']

        diagnol2 = set([board[0][2], board[1][1], board[2][0]])
        if len(diagnol2) == 1 and -1 not in diagnol2:
            return True, models.BOARD_LOOKUP[diagnol2.pop()]['long']

        for row in board:
            if -1 in row:
                return False, None
        return True, None
