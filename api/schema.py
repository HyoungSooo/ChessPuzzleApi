from ninja import Schema
from typing import List


class PuzzleOut(Schema):
    puzzleid: str
    rating: str
    fen: str
    tag: str
    gameurl: str


class Error(Schema):
    message: str


class PuzzlewithMoveOut(Schema):
    puzzleid: str
    tag: str
    fen: str
    move: List


class ThemeOut(Schema):
    theme: str


class OpeningOut(Schema):
    opening: str
