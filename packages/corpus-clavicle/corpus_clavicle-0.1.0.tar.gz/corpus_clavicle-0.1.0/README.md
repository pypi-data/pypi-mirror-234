## corpus-clavicle

This is a python package used to provide models and auxilaries for the corpus package for dealing with total proteomics data

## Installation

```bash
pip install django-postgres-extra corpus-clavicle psycopg2 
```

## Usage

```python
import os
INSTALLED_APPS = [
    #...
    'django.contrib.postgres',  # Required for 'psqlextra
    'psqlextra',
    'clavicle',
    #...
]

DATABASE_ROUTERS = ['clavicle.dbrouter.ClavicleRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
    'clavicle': {
        'ENGINE': 'psqlextra.backend',
        'NAME': os.environ.get('POSTGRES_NAME', 'clavicle'),
        'USER': os.environ.get('POSTGRES_USER', 'admin'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', "testpostgrest"),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': int(os.environ.get('POSTGRES_PORT', '5432')),
    }
}
```

```bash
python manage.py migrate --database=clavicle
```





