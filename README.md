# Simple Flask Auth App

Just a simple Flask app to demo coding abilities.

Inspired by (and heavily based on): https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb

"Email" confirmation inspired by: https://github.com/MaxHalford/flask-boilerplate

Comes with Dockerfile and docker-compose.yml files for testing.

Disclaimer: This code is not meant for full production use. It is more an introduction to some core concepts.

## Dependencies

This project depends on Python 3. Specifically, this was developed against Python 3.7.

[Pipenv](https://docs.pipenv.org/) is used for dependency management, see the `Pipfile`.

Docker is used for the development environment.

## Dev environment

You can set up the dev environment with:
- Docker: Run `build.sh` then `run.sh` to start the development server.
- docker-compose: Run `docker-compose up` to bring up the server.
- Use `pipenv install` to install the dependencies and then run the Flask server with
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


