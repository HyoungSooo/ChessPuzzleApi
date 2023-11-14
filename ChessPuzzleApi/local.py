from .settings import *

SECRET_KEY = 'supersecrets'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite3.db',  # This is where you put the name of the db file.
        # If one doesn't exist, it will be created at migration time.
    }
}
