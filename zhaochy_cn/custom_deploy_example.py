def customize(BASE_DIR):
    '''
          production environment
    '''

    # SECURITY WARNING: don't run with debug turned on in production!

    DEBUG = False

    ALLOWED_HOSTS = [
        '*',
    ]

    # Database
    # https://docs.djangoproject.com/en/1.8/ref/settings/#databases

    DATABASES = {

        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            'OPTIONS': {

            },
        }
    }

    SESSION_ENGINE = "django.contrib.sessions.backends.file"

    return DEBUG, ALLOWED_HOSTS, DATABASES, SESSION_ENGINE
