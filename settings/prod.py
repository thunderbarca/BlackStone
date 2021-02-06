from settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django',
        'USER': 'postgres',
        'PASSWORD': 'sh@dow',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
