DATABASE = {
    'user': 'tictactoe',
    'password': 'tictactoe',
    'database': 'tictactoe',
    'host': '127.0.0.1',
}

DATABASE_URL = 'postgresql+psycopg2://{user}:{password}@{host}/{database}'.format(**DATABASE)
