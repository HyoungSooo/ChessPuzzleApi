# ninja
from ninja import NinjaAPI, Field
from ninja.pagination import paginate, LimitOffsetPagination
from ninja.schema import Schema

# django
from django.db import connection
from django.db.models import QuerySet
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.db.models.functions import Length
from django.db.models import Case, When, Value

# others
from typing import Any, List
from api.models import *
import random
api = NinjaAPI(openapi_url=settings.DEBUG and "/openapi.json" or "")


class CustomLimitPagination(LimitOffsetPagination):
    class Input(Schema):
        limit: int = Field(settings.NINJA_PAGINATION_PER_PAGE, ge=1)
        offset: int = Field(0, ge=0)

    def paginate_queryset(self, queryset: QuerySet, pagination: Input, **params: Any) -> Any:
        pagination.limit = min(
            settings.NINJA_PAGINATION_MAX_PER_PAGE, pagination.limit)

        return super().paginate_queryset(queryset, pagination, **params)


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


class Error(Schema):
    message: str


@api.get('/puzzle', response=List[PuzzleOut])
@paginate(CustomLimitPagination)
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
@paginate(CustomLimitPagination)
def get_puzzle_specific_rating(request, rating: int):
    return Puzzle.objects.filter(rating__gte=rating - 100, rating__lte=rating)


@api.get('/rating/range', response=List[PuzzleOut])
@paginate(CustomLimitPagination)
def get_puzzle_range_of_rating(request, max: int, min: int):
    return Puzzle.objects.filter(rating__gte=min, rating__lte=max)


@api.get('/tag', response=List[PuzzleOut])
@paginate(CustomLimitPagination)
def get_puzzle_specific_difficulty_level(request, tag: str):
    return Puzzle.objects.filter(tag__iexact=tag)


@api.get('/puzzle/rush', response={200: List[PuzzleOut], 400: Error})
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


urlpatterns = [
    path('', api.urls),
    path('index/', TemplateView.as_view(template_name='index.html'))
]
