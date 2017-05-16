# Diploma thesis on the FIT CTU (FIT ČVUT).

Project requirements:
- Python version 3.5 or higher
- virtualenv
- MySQL server
- PIP for Python in version 3.*

Clone this repository using:
```
git clone https://github.com/marekhanacek/diploma-thesis-app
```

Setup environment variables using:
```
virtualenv __env__
source __env__/bin/activate

export DJANGO_SECRET_KEY={secret_key}
export DATABASE_NAME=dip
export DATABASE_USER=root
export DATABASE_PASS=*******
export DATABASE_HOST=localhost
export SOCIAL_AUTH_FACEBOOK_KEY={facebook_app_key}
export SOCIAL_AUTH_FACEBOOK_SECRET={facebook_app_secret}
export STATIC_ROOT=/var/www/MI-DIP/dipweb/static/
export DJANGO_DEBUG=TRUE
# email settings
export EMAIL_ALLOW_MAIL_SENDING=TRUE
export EMAIL_USE_SSL=TRUE
export EMAIL_USE_TLS=FALSE
export EMAIL_HOST_PASSWORD=*******
export EMAIL_FROM=hanacma3@fit.cvut.cz
export EMAIL_HOST=imap.fit.cvut.cz
export EMAIL_HOST_USER=hanacma3
export EMAIL_PORT=465
```

Create database in MySQL. Name should be equal to `DATABASE_NAME`.

Install requirements:
```
pip install -r requirements.txt
```

Install migrations:
```
python manage.py migrate
```

Install minimal test data:
```
python manage.py loaddata fixtures/initial_data.json
```

Run server:
```
python manage.py runserver
```

Application should be now available on http://localhost:8000.