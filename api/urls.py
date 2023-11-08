from django.urls import path
from ninja import NinjaAPI
from ninja.pagination import paginate
from ninja.schema import Schema
from typing import List
from django.db import connection
from api.models import *
import random
from django.views.generic import TemplateView

api = NinjaAPI()


def get_puzzle_moves_from_database(id):
    query = f'''
        SELECT p.puzzleid, p.tag, p.fen, m.move, m.number from (select puzzleid, tag, fen from puzzle where puzzleid = '{id}') as p join (select a.move, b.puzzleid, b.number from move as a join
        puzzle_move as b on a.idx = b.idx) as m on p.puzzleid = m.puzzleid;
    '''
    cursor = connection.cursor()
    result = cursor.execute(query)
    total_moves = cursor.fetchall()

    move = [move[0] for move in sorted(
        [(i[3:]) for i in total_moves], key=lambda x: x[-1])]

    return PuzzlewithMoveOut(puzzleid=id, tag=total_moves[0][1], move=move, fen=total_moves[0][2])


class PuzzleOut(Schema):
    puzzleid: str
    rating: str
    fen: str
    tag: str
    gameurl: str


@api.get('/puzzle', response=List[PuzzleOut])
@paginate
def get_puzzle(request):
    return Puzzle.objects.all()


class PuzzlewithMoveOut(Schema):
    puzzleid: str
    tag: str
    fen: str
    move: List


@api.get('/puzzle/move', response=PuzzlewithMoveOut)
def get_puzzle_move(request, puzzleid):
    res = get_puzzle_moves_from_database(puzzleid)

    return res


class ThemeOut(Schema):
    theme: str


@api.get('/theme', response=List[ThemeOut])
def get_all_theme(request):
    return Theme.objects.all()


@api.get('/theme/puzzle', response=PuzzlewithMoveOut)
def get_puzzle_in_theme(request, theme):
    query = f'''
        Select p.puzzleid, theme from puzzle_theme as p join (select * from theme where theme = '{theme}') as t on t.idx = p.idx;
    '''

    cursor = connection.cursor()
    result = cursor.execute(query)
    puzzles_on_theme = cursor.fetchall()
    random_select_puzzle = random.choice(puzzles_on_theme)
    puzzle_id = random_select_puzzle[0]

    return get_puzzle_moves_from_database(puzzle_id)


@api.get('/rating', response=List[PuzzleOut])
@paginate
def get_puzzle_specific_rating(request, rating: int):
    return Puzzle.objects.filter(rating__gte=rating - 100, rating__lte=rating)


@api.get('/rating/range', response=List[PuzzleOut])
@paginate
def get_puzzle_range_of_rating(request, max: int, min: int):
    return Puzzle.objects.filter(rating__gte=min, rating__lte=max)


urlpatterns = [
    path('', api.urls),
    path('index/', TemplateView.as_view(template_name='index.html'))
]
