# Django Two Factor example

## Requirements

- Docker Compose

```bash
# Project env vars
DEBUG=1
SECRET_KEY=
DJANGO_ALLOWED_HOSTS=*


SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432

# This hash will be used for the token encryption later on.
HASHING_SECRET=some_thing

#Aws things
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_SES_REGION_NAME=

#Email things
EMAIL_FROM=
FROM_NAME=
```

**You should create a .env folder and a django file inside it.**


- To build the entire project, we enter the following command:

```bash
docker-compose build
```

- Once that is done, we execute the command to bring up all the instances:

```bash
docker-compose up
```

- To generate superusers, use the following command:

```bash
docker-compose run --rm web python manage.py createsuperuser
```

- After that, you can access `localhost:8000` in your browser.


### The defined URLs are as follows.

- `localhost:8000/login` At that URL, you have access to the login page.

- `localhost:8000/dashboard` At that URL, you have access to the dashboard. ONLY LOGGED
- `localhost:8000/two_factor/` That URL is the section where the authentication factor is generated, and access is only possible with a specific token that is stored in the server's cache and is auto-generated uniquely.


#### Templates source:

- Email https://github.com/konsav/email-templates/

- Login https://mdbootstrap.com/docs/standard/extended/login/