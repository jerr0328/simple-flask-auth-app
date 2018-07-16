# Simple Flask Auth App

[![Build Status](https://travis-ci.org/jerr0328/simple-flask-auth-app.svg?branch=master)](https://travis-ci.org/jerr0328/simple-flask-auth-app)

Just a simple Flask app to demo coding abilities.

Inspired by (and heavily based on): https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb

"Email" confirmation inspired by: https://github.com/MaxHalford/flask-boilerplate

Comes with Dockerfile and docker-compose.yml files for testing.

**Disclaimer: This code is not meant for full production use. It is more an introduction to some core concepts.**

## Dependencies

This project depends on Python 3. Specifically, this was developed against Python 3.6.

[Pipenv](https://docs.pipenv.org/) is used for dependency management, see the `Pipfile`.

Docker is used for the development environment, although it also works in Pipenv (see below).

## Dev environment

You can set up the dev environment with:
- Docker: Run `build.sh` then `run.sh` to start the development server.
- docker-compose: Run `docker-compose up` to bring up the server.
- Use `pipenv install --dev` to install the dependencies and then run the Flask server with
`FLASK_APP=main flask run`. You can also set the development mode with the `FLASK_DEBUG=1` or `FLASK_ENV=development`
environment variables.


## Future improvements

This project is relatively barebones and still has a lot that can be improved.

- Use more secure password hashing
- Follow OWASP suggestions
- Enable WSGI server (e.g. uwsgi, gunicorn)
- Better manage DB migrations
- Handle email confirmation
- Unit/integration testing
- Allow for different configurations via files and environment variables
- Use a database server like Postgresql
- Better support for blacklisting JWT tokens (e.g. using Redis or periodically cleaning the blacklist table)
- CI with Travis/CircleCI

## Decisions

This project uses JSON Web Tokens (JWT) for authentication. This is done to enable authentication without sending the username and password with each request (as with HTTP Basic Auth), and is becoming a more popular choice for APIs.
The secret keys used here are not secure by any means, and should not be used in a production environment.

SQLite is used as a backend in order to avoid bogging this project down in database setup. Ensuring that Postgres is up before the application takes some tinkering with Docker-compose, and this is not in the scope of this project.

Flask-RESTful makes it a lot easier to just set up functions that handle different HTTP verbs.

SQLAlchemy gives a nice ORM to use, and is pretty standard in Flask applications.

Passlib is used since it was in the examples on how to set up a Flask application with JWT. Flask-BCrypt might be a better replacement (see Future Improvements section above).

Initial tests written cover ~70% of total code and most of the core code. It does not check the testing tools like the users endpoint nor the logout feature.

