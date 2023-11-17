# ninja
from ninja_extra import NinjaExtraAPI

# django
from django.urls import path
from django.conf import settings

# auth
from ninja_jwt.controller import NinjaJWTDefaultController

# router
from jwt_auth.router import router as auth_router
from api.routers.puzzle_router import router as puzzle_router
from api.routers.puzzle_opening import router as opening_router

api = NinjaExtraAPI()

api.register_controllers(NinjaJWTDefaultController)
api.add_router(router=auth_router, prefix='auth', tags=['auth'])
api.add_router(router=puzzle_router, prefix='puzzle', tags=['puzzle'])
api.add_router(router=opening_router, prefix='opening', tags=['opening'])

urlpatterns = [
    path('', api.urls),

]
