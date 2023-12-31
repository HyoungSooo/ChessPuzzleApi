# Generated by Django 4.0 on 2023-11-06 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Move',
            fields=[
                ('idx', models.IntegerField(primary_key=True, serialize=False)),
                ('move', models.CharField(blank=True, max_length=6, null=True)),
            ],
            options={
                'db_table': 'move',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Puzzle',
            fields=[
                ('idx', models.IntegerField(primary_key=True, serialize=False)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('puzzleid', models.CharField(blank=True, max_length=6, null=True, unique=True)),
                ('fen', models.TextField(blank=True, null=True)),
                ('tag', models.CharField(blank=True, max_length=6, null=True)),
                ('gameurl', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'puzzle',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PuzzleMove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'puzzle_move',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PuzzleTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'puzzle_theme',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('idx', models.IntegerField(primary_key=True, serialize=False)),
                ('theme', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'theme',
                'managed': False,
            },
        ),
    ]
