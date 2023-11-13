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

api = NinjaExtraAPI(
    openapi_url=settings.DEBUG and "/openapi.json" or "")

api.register_controllers(NinjaJWTDefaultController)
api.add_router(router=auth_router, prefix='auth')
api.add_router(router=puzzle_router, prefix='puzzle')

urlpatterns = [
    path('', api.urls),

]
