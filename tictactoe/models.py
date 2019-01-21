from tictactoe.database import db

EMPTY = -1
CIRCLE = 0
CROSS = 1

EMPTY_BOARD = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]

BOARD_LOOKUP = {
    CIRCLE: {'short': 0, 'long': 'circle'},
    CROSS: {'short': 1, 'long': 'cross'},
    EMPTY: {'short': None, 'long': None},
}

def pretty_board(board):
    pretty_board = []
    for row in board:
        pretty_board.append([BOARD_LOOKUP[space]['short'] for space in row])
    return pretty_board

class Games(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    circle = db.Column(db.String(80), nullable=False)
    cross = db.Column(db.String(80), nullable=False)
    board = db.Column(db.ARRAY(db.Integer, dimensions=2, zero_indexes=True), nullable=False)
    next_turn = db.Column(db.String(6), nullable=True)
    closed = db.Column(db.Boolean, nullable=False, server_default='f')
    winner = db.Column(db.String(6), nullable=True)

    def dictify(self, pretty=True):
        return {
            'id': self.id,
            'circle': self.circle,
            'cross': self.cross,
            'board': pretty_board(self.board) if pretty else self.board,
            'next_turn': self.next_turn,
            'closed': self.closed,
            'winner': self.winner,
        }
