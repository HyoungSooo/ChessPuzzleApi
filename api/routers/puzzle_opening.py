# ninja
from ninja_extra import Router
from ninja.pagination import paginate
from ninja.errors import HttpError

# django
from django.db import connection
from django.db.models import F

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


@router.get('/category', response=List[OpeningOut])
@paginate(CustomLimitPagination)
def get_opening_list(request):
    query = """
        SELECT tag from openingtag;
    """

    cursor = connection.cursor()
    result = cursor.execute(query)
    opening_list = cursor.fetchall()

    response = list(map(lambda x: {'opening': x[0]}, opening_list))

    return response


@router.get('/search', response={200: List[OpeningOut], 400: Error})
@paginate(CustomLimitPagination)
def search_opening_name_with_like_method(request, query: str):
    if len(query) < 2:
        print(query)
        raise HttpError(400, "query must long then two charactors")

    qs = Openingtag.objects.filter(tag__icontains=query).annotate(
        opening=F('tag')).values('opening')

    return qs


@router.get('/puzzle', response={200: List[PuzzleOut], 400: Error})
@paginate(CustomLimitPagination)
def get_puzzle_in_opening(request, opening: str):
    sql = f'''
        Select p.puzzleid, p.gameurl, p.fen, p.tag, p.rating from (select k.puzzleid, k.gameurl, k.fen, k.tag, k.rating, p.idx from puzzle_opening as p join puzzle as
        k on p.puzzleid = k.puzzleid) as p join (select * from openingtag where tag = '{opening}') as t on t.idx = p.idx
    '''
    cursor = connection.cursor()
    result = cursor.execute(sql)
    opening_puzzle_list = cursor.fetchall()

    if not opening_puzzle_list:
        return HttpError(400, "No Response")

    response = res = list(map(lambda x: {
        'puzzleid': x[0], 'gameurl': x[1], 'fen': x[2], 'tag': x[3], 'rating': x[4]}, opening_puzzle_list))

    return response
