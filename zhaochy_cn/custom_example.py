def customize(BASE_DIR):
    '''
    develop environment
    '''

    # SECURITY WARNING: don't run with debug turned on in production!

    DEBUG = True

    ALLOWED_HOSTS = [
        '*',
    ]

    # Database
    # https://docs.djangoproject.com/en/1.8/ref/settings/#databases

    DATABASES = {

        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '',  # database name
            'USER': '',  # mysql username
            'PASSWORD': '',  # mysql password
            'HOST': 'localhost',  # mysql host
            'PORT': '3306',  # default port
            'OPTIONS': {
                'charset': 'utf8',  # support unicode
            },
        }
    }

    SESSION_ENGINE = "django.contrib.sessions.backends.file"

    return DEBUG, ALLOWED_HOSTS, DATABASES, SESSION_ENGINE
