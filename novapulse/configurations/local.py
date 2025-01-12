
from .base import *

DATABASES = {
    'default': {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'novapulse',
        "USER": 'postgres',
        "PASSWORD": 'postgres',
        "HOST": 'localhost',
        "PORT": 5432,
    }
}