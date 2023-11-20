# ninja
from api.schema import *
from ninja_extra import Router
from ninja.pagination import paginate

# django
from django.db import connection


def get_puzzle_moves_from_database(id):
    query = f'''
        SELECT p.puzzleid, p.tag, p.fen, m.move, m.number from (select puzzleid, tag, fen from puzzle where puzzleid = '{id}') as p join (select a.move, b.puzzleid, b.number from move as a join
        puzzle_move as b on a.idx = b.idx) as m on p.puzzleid = m.puzzleid;
    '''
    cursor = connection.cursor()
    result = cursor.execute(query)
    total_moves = cursor.fetchall()

    if not total_moves:
        return False

    move = [move[0] for move in sorted(
        [(i[3:]) for i in total_moves], key=lambda x: x[-1])]

    return {'puzzleid': id, 'tag': total_moves[0][1], 'move': move, 'fen': total_moves[0][2]}
