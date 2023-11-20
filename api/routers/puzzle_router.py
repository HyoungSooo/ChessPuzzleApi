# ninja
from ninja_extra import Router
from ninja.pagination import paginate

# django
from django.db import connection
from django.db.models import QuerySet
from django.db.models import Case, When, Value

# others
from typing import List
from api.models import *
from api.routers.utils import get_puzzle_moves_from_database

# auth
from jwt_auth.barrer import JWTAuthRequired

# pagination
from api.pagination import CustomLimitPagination

# schema
from api.schema import *


router = Router(auth=JWTAuthRequired())


@router.get('', response=List[PuzzleOut])
@paginate(CustomLimitPagination)
def get_puzzle(request):
    return Puzzle.objects.all()


@router.get('/move', response={200: PuzzlewithMoveOut, 400: Error})
def get_puzzle_move(request, puzzleid):
    res = get_puzzle_moves_from_database(puzzleid)

    if not res:
        return 400, {'message': 'invalid puzzleid'}

    return PuzzlewithMoveOut(**res)


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
