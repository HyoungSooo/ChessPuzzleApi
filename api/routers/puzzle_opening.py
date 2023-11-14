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
