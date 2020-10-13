# django-poll
Django poll API


- Initiate python environment
```
$ pip install pipenv
```

- Install dependencies
```
$ pipenv install -r requirements.txt
```

- Showmigrations and migrate
```
$ python manage.py showmigrations
$ python manage.py migrate
```

- Runserver
```
$ export PYTHONUNBUFFERED=1
$ python manage.py runserver
```
Your server should be ready at localhost:8000

- Allowed endpoints
```
POST /v1/user
GET /v1/campaign
GET /v1/campaign/:id
POST /v1/campaign
POST /v1/option
POST /v1/poll
```

- Other useful commands
```
// Create superuser
$ python manage.py createsuperuser

// Run tests
$ python manage.py test

// Django interactive shell
$ python manage.py shell
>>> from user.models import *
>>> from poll.models import *
>>> 
>>> User.objects.all()  # list all users
>>> Option.objects.get(id='foo').polls.count()  # poll count of an option
>>> Campaign.objects.last().options.all()  # last campaign's options
```