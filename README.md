# Pretenders server

Pretenders server description.

### Prerequisites

- Start by ensuring that you have Docker, Docker Compose, and Docker Machine installed:

```
$ docker -v
Docker version 17.03.1-ce, build c6d412e
$ docker-compose -v
docker-compose version 1.11.2, build dfed245
$ docker-machine -v
docker-machine version 0.10.0, build 76ed2a6
```

Docker is really all you need. That's all.

### Installing


Build the image:
```
docker-compose up -d --build
```

\
This will take a few minutes the first time. Subsequent builds will be much faster since 
Docker caches the results of the first build. Once done, fire up the container:
```
docker-compose up -d
```

> The -d flag is used to run the containers in the background.\
> However, you don't have any logs from containers with the -d flag.

You can run the following command to verify if your containers are running and up. 
```
docker ps -a

CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS              PORTS                    NAMES
ca6b523a9209        git_pretenders_db       "docker-entrypoint.s…"   2 hours ago         Up 2 hours          0.0.0.0:5435->5432/tcp   pretenders_db
8128bbba7d90        git_pretenders_server   "python manage.py ru…"   2 hours ago         Up 2 hours          0.0.0.0:5001->5000/tcp   pretenders_server
```

\
Next you have to re/create the database:
```
docker-compose run pretenders_server python manage.py recreate-database
```

\
Server will be opened for the url : http://docker-machine-ip:5001/
> Take a look at docker-compose.yml for more informations.
 
## Running the tests

You can run tests with the following command : 
```
docker-compose run pretenders_server python manage.py test
```
You can also run the command 
```
python manage.py test
```
inside of the pretenders_server container.

\
In order to go inside of a container run :
```
docker ps -a

CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS              PORTS                    NAMES
ca6b523a9209        git_pretenders_db       "docker-entrypoint.s…"   2 hours ago         Up 2 hours          0.0.0.0:5435->5432/tcp   pretenders_db
8128bbba7d90        git_pretenders_server   "python manage.py ru…"   2 hours ago         Up 2 hours          0.0.0.0:5001->5000/tcp   pretenders_server
``` 

Keep in mind the container_id of the pretenders_server and run the command : 
```
docker exec -it container_id sh
``` 
> If you run docker on Windows OS you need to prefix the command with 'winpty'

## Postgres commands

In order to go inside of the postgres container run the command below: 
```
$ winpty docker exec -it container_id sh
/ #  psql -U postgres
psql (10.4)
Type "help" for help.

postgres=#
```

You can connect into a specific database with the command : 
```
\c users_dev
You are now connected to database "users_dev" as user "postgres".
users_dev=#
```

You can list tables with the command : 
```
users_dev=# \dt
              List of relations
 Schema |       Name       | Type  |  Owner
--------+------------------+-------+----------
 public | blacklist_tokens | table | postgres
 public | users            | table | postgres
(2 rows)

users_dev=#

```

### Coding style tests

Python has its own coding style - called pep8 - that we expect you to respect.\
 - [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
 > Some IDEs supports continuous checking of your code for PEP 8 compliance on the fly, as you type it in the editor. (JetBrains IDEs)

## Deployment


## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - Python IDE for Professional Developers
* [PostgreSQL](https://www.postgresql.org/) - PostgreSQL is an object-relational database management system 
(ORDBMS).
* [Flask](http://flask.pocoo.org/) - Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.

## Authors
* **Gajovski Maxime** - *Initial work* 

## TO DOs