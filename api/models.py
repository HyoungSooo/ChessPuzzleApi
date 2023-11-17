# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Move(models.Model):
    idx = models.IntegerField(primary_key=True)
    move = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'move'


class Puzzle(models.Model):
    idx = models.IntegerField(primary_key=True)
    rating = models.IntegerField(blank=True, null=True)
    puzzleid = models.CharField(
        unique=True, max_length=6, blank=True, null=True)
    fen = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=6, blank=True, null=True)
    gameurl = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'puzzle'


class PuzzleMove(models.Model):
    puzzleid = models.ForeignKey(
        Puzzle, models.DO_NOTHING, to_field='puzzleid', db_column='puzzleid', blank=True, null=True)
    idx = models.ForeignKey(Move, models.DO_NOTHING,
                            to_field='idx', db_column='idx', blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'puzzle_move'


class PuzzleTheme(models.Model):
    puzzleid = models.ForeignKey(
        Puzzle, models.DO_NOTHING, to_field='puzzleid', db_column='puzzleid', blank=True, null=True)
    idx = models.ForeignKey('Theme', models.DO_NOTHING,
                            to_field='idx', db_column='idx', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'puzzle_theme'


class Theme(models.Model):
    idx = models.IntegerField(primary_key=True)
    theme = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'theme'


class Openingtag(models.Model):
    idx = models.AutoField(primary_key=True)
    tag = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'openingtag'


class PuzzleOpening(models.Model):
    puzzleid = models.ForeignKey(
        Puzzle, models.DO_NOTHING, db_column='puzzleid', blank=True, null=True)
    idx = models.ForeignKey(Openingtag, models.DO_NOTHING,
                            db_column='idx', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'puzzle_opening'
