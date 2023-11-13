# ninja
from ninja_extra import Router
from ninja.pagination import paginate
from ninja.schema import Schema

# django
from django.db import connection
from django.db.models import QuerySet
from django.urls import path
from django.db.models import Case, When, Value

# others
from typing import List
from api.models import *

# auth
from jwt_auth.barrer import JWTAuthRequired

# pagination
from api.pagination import CustomLimitPagination

# schema
from api.schema import *


router = Router(auth=JWTAuthRequired())


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

    return PuzzlewithMoveOut(puzzleid=id, tag=total_moves[0][1], move=move, fen=total_moves[0][2])


@router.get('', response=List[PuzzleOut])
@paginate(CustomLimitPagination)
def get_puzzle(request):
    return Puzzle.objects.all()


@router.get('/move', response={200: PuzzlewithMoveOut, 400: Error})
def get_puzzle_move(request, puzzleid):
    res = get_puzzle_moves_from_database(puzzleid)

    if not res:
        return 400, {'message': 'invalid puzzleid'}

    return res


@router.get('/theme/category', response=List[ThemeOut])
def get_all_theme(request):
    return Theme.objects.all()


@router.get('/theme', response=List[PuzzleOut])
@paginate(CustomLimitPagination)
def get_puzzle_in_theme(request, theme):
    query = f'''
        Select p.puzzleid, p.gameurl, p.fen, p.tag, p.rating from (select k.puzzleid, k.gameurl, k.fen, k.tag, k.rating, p.idx from puzzle_theme as p join puzzle as
        k on p.puzzleid = k.puzzleid) as p join (select * from theme where theme = '{theme}') as t on t.idx = p.idx
    '''

    cursor = connection.cursor()
    result = cursor.execute(query)
    puzzles_on_theme = cursor.fetchall()

    res = list(map(lambda x: {
               'puzzleid': x[0], 'gameurl': x[1], 'fen': x[2], 'tag': x[3], 'rating': x[4]}, puzzles_on_theme))

    return res


@router.get('/rating', response=List[PuzzleOut])
@paginate(CustomLimitPagination)
def get_puzzle_specific_rating(request, rating: int):
    return Puzzle.objects.filter(rating__gte=rating - 100, rating__lte=rating)


@router.get('/rating/range', response=List[PuzzleOut])
@paginate(CustomLimitPagination)
def get_puzzle_range_of_rating(request, max: int, min: int):
    return Puzzle.objects.filter(rating__gte=min, rating__lte=max)


@router.get('/tag', response=List[PuzzleOut])
@paginate(CustomLimitPagination)
def get_puzzle_specific_difficulty_level(request, tag: str):
    return Puzzle.objects.filter(tag__iexact=tag)


@router.get('/rush', response={200: List[PuzzleOut], 400: Error})
def puzzle_rush(request, num: int = 50, easy: int = 10, normal: int = 30, hard: int = 10):
    if num > 100:
        return 400, {'message': "Number of puzzle must less than 100"}

    easy = Puzzle.objects.filter(tag__iexact='easy').order_by('?')[:easy]
    normal = Puzzle.objects.filter(tag__iexact='normal').order_by('?')[:normal]
    hard = Puzzle.objects.filter(tag__iexact='hard').order_by('?')[:hard]

    qs: QuerySet = easy | normal | hard

    qs = qs.annotate(tag_sub=Case(
        When(tag__iexact='easy', then=Value(1)),
        When(tag__iexact='normal', then=Value(2)),
        When(tag__iexact='hard', then=Value(3)),
    ))

    return qs.order_by('tag_sub').only(
        'puzzleid',
        'rating',
        'fen',
        'tag',
        'gameurl'
    )
