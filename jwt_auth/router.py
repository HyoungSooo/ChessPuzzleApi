from jwt_auth.schemas import AuthSchema, Message
from ninja import Router
from jwt_auth.models import User

# validation
from jwt_auth.validation import check_getted_user_informations

router = Router()


@router.post('/register', auth=None, response={200: Message, 400: Message})
def register_user(request, auth: AuthSchema):
    if check_getted_user_informations(username=auth.username, password=auth.password, email=auth.email):
        user = User.objects.create_user(
            username=auth.username, email=auth.email, password=auth.password)
        return 200, {'message': user.username}

    return 400, {'message': 'Invalid username or password or email. (Username pattern: alphanumeric characters and underscores, 3 to 20 characters), (Password pattern: at least 8 characters, at least one uppercase letter, one lowercase letter, and one digits)'}
