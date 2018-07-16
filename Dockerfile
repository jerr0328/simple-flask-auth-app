FROM kennethreitz/pipenv
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/
COPY . /app
EXPOSE 5000
ENV FLASK_APP main
ENV FLASK_ENV development
ENV FLASK_DEBUG 1
ENV SFAA_SETTINGS 'config/dev.py'
CMD flask run --host=0.0.0.0