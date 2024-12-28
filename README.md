# "Planetarium API Service"

Python Django REST framework project.

This project provides an API for managing ticket bookings for planetarium sessions.
The main functionality includes session scheduling, ticket booking, and session administration.

## Description

The service allows:

- Viewing session schedules (for registered users).
- Booking tickets (for registered users).
- Managing bookings (deleting and updating available only for administrators).
- Administering schedules (creating, updating, and deleting sessions available only for administrators).

## Technologies

- Python 3
- Django 5
- Django REST framework
- SQL (Postgres)
- Docker
- JWT for authentication

## Features

- JWT authenticated
- admin panel /admin/
- documentation is located at /api/doc/swagger/
- managing reservation and tickets
- creating astronomy show with themes
- creating astronomy dome
- adding astronomy show sessions
- filtering astronomy show by theme and title
- filtering astronomy show session by show and datetime


## Installation

1. Install Python3:

```shell
www.python.org/
```

2. Install Git:

```shell
git-scm.com/
```

3. Clone the repository.

main branch:
```shell
git clone https://github.com/skyfoxwork/planetarium.git
```

develop branch

```shell
git clone -b develop https://github.com/skyfoxwork/planetarium.git
```

4. Navigate to the project directory:

```shell
cd planetarium
```

5. Set up environment variables: Create a .env file in the root directory and add the following (use .env.sample):
```shell
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_user
POSTGRES_HOST=db
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data
```

6. Run the application using Docker:
```shell
docker-compose build
docker-compose up
```

7.Optional:

Run  and create a superuser and fill database with data:
```shell
docker ps
```
you will see:
```shell
CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS          PORTS                    NAMES
d5b41340d460   planetarium-app      "sh -c 'python manag…"   14 seconds ago   Up 13 seconds   0.0.0.0:8000->8000/tcp   planetarium-app-1
9d3467a13ee6   postgres:14-alpine   "docker-entrypoint.s…"   14 seconds ago   Up 13 seconds   0.0.0.0:5433->5432/tcp   planetarium-db-1
```
use:
```shell
docker exec -it <CONTAINER ID> bash
```
Create super user:
```shell
python manage.py createsuperuser
```

Fill database with data:
```shell
python manage.py loaddata planetarium_fixture.json
```
```shell
exit
```

11. Visit your web browser:

```shell
http://localhost:8000/api/planetarium/ or http://127.0.0.1:8000/api/planetarium/
```
to log in:
user:
```shell
username: user@example.com
password: userexample123
```
admin:
```shell
username: admin@example.com
password: adminexample245
```
or you can create your superuser with:

```shell
python3 manage.py createsuperuser
```

and login as your custom superuser.

12. Access the application:
API is available at: 
```shell
http://localhost:8000/api/
```
Swagger documentation is available at:
```shell
http://localhost:8000/api/docs/
http://localhost:8000/api/doc/swagger/
```
