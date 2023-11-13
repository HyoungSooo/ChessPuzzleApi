import re
from jwt_auth.schemas import AuthSchema, Message
from ninja import Router
from jwt_auth.models import User

router = Router()


def is_valid_email(email):
    regex = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None


@router.post('/register', auth=None, response={200: Message, 400: Message})
def register_user(request, auth: AuthSchema):
    if is_valid_email(auth.email):
        user = User.objects.create_user(
            username=auth.username, email=auth.email, password=auth.password)
        return 200, {'message': user.username}

    return 400, {'message': 'invaild email'}
