import re
from ninja.errors import HttpError


def is_valid_username(username):
    # Username pattern: alphanumeric characters and underscores, 3 to 20 characters
    pattern = re.compile(r'^[a-zA-Z0-9_]{3,20}$')
    return bool(pattern.match(username))


def is_valid_password(password):
    # Password pattern: at least 8 characters, at least one uppercase letter, one lowercase letter, and one digit
    pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
    return bool(pattern.match(password))


def is_valid_email(email):
    regex = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None


def check_getted_user_informations(username: str, password: str, email: str):
    if is_valid_username(username) and is_valid_password(password) and is_valid_email(email):
        return True
    else:
        return False
