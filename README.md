# Tic Tac Toe Challenge

## Setup and run:
Written in python 3.7.1. Postgres used for database.

```
pip install -r requirements.txt
pip install -U .
python tictactoe/app.py
```

## Playing
Create a game:
```
requests.post('http://localhost:5000/api/games', headers={'content-type': 'application/json'}, data=json.dumps({'player1': 'foo', 'player2': 'bar'}))
```

Which returns you back a newly created game with an ID and who will go first:

```
 {'id': 31,
 'circle': 'bar',
 'cross': 'foo',
 'board': [[None, None, None], [None, None, None], [None, None, None]],
 'next_turn': 'cross',
 'closed': False,
 'winner': None}
```

You can then post to make your move. Game spaces are ordered by passing a coordinate value. Coordinates for the board:
```
(0, 0) | (0, 1) | (0, 2)
------------------------
(1, 0) | (1, 1) | (1, 2)
------------------------
(2, 0) | (2, 1) | (2, 2)
```

```
requests.post('http://localhost:5000/api/games/31', headers={'content-type': 'application/json'}, data=json.dumps({'player': 'foo', 'x': 2, 'y': 1})); resp.status_code, resp.json()
```

Which will return you the game state:

```
 {'id': 31,
  'circle': 'bar',
  'cross': 'foo',
  'board': [[None, None, None], [None, None, None], [None, 1, None]],
  'next_turn': 'circle',
  'closed': False,
  'winner': None}
```

## Implementation/Analysis
The implementation is done using Flask with a couple of helpful plugins.

* Flask-RESTful: Handled a lot of the boilerplate for creating REST APIs
* FlaskSQLAlchemy: For the model and database communication layer

A single "Games" model is stored in the database. There's a few design choices to be made here, but the most interesting is the board. Since postgres was used for the database, SQLAlchemy has support for multidimensional arrays, so a 2D integer array was stored in the database

The rest of the API is pretty straight forward, though a few shortcuts were made (specifically in regards to some getattr's). There's an interesting Flask-SQLAlchemy issue when trying to update a 2D Array, hence a terrible double statement execution. The game_state function is also grizzly to say the least. Both of which could use refactoring and optimizations.
