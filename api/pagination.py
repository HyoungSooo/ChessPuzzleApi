# ninja
from ninja import Field
from ninja.pagination import LimitOffsetPagination
from ninja.schema import Schema

# django
from django.db.models import QuerySet
from django.conf import settings

# others
from typing import Any


class CustomLimitPagination(LimitOffsetPagination):
    class Input(Schema):
        limit: int = Field(settings.NINJA_PAGINATION_PER_PAGE, ge=1)
        offset: int = Field(0, ge=0)

    def paginate_queryset(self, queryset: QuerySet, pagination: Input, **params: Any) -> Any:
        pagination.limit = min(
            settings.NINJA_PAGINATION_MAX_PER_PAGE, pagination.limit)

        return super().paginate_queryset(queryset, pagination, **params)
