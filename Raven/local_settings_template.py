DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Project Root Dir
PROJECT_ROOT_DIR = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@_ixep2ox2d#c3cf)x9r4#4l@q70e&amp;o&amp;l1d#po=er%x%1_+2aq'