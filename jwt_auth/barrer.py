from typing import Any, Optional
from django.http import HttpRequest
from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache


class JWTAuthRequired(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        jwt_authenticator = JWTAuthentication()
        try:
            response = jwt_authenticator.authenticate(request)
            if response is not None:
                if cache.get(response[0].username):
                    return False
                else:
                    cache.set(response[0].username, 'done', 5)
                    return response[0].username  # 200 OK
            return False  # 401
        except Exception:
            # Any exception we want it to return False i.e 401
            return False
