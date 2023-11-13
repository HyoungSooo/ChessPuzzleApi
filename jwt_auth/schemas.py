from ninja import Schema


class AuthSchema(Schema):
    username: str
    password: str
    email: str


class JWTPairSchema(Schema):
    refresh: str
    access: str


class Message(Schema):
    message: str
