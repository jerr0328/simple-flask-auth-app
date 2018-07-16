#!/usr/bin/env bash

docker run -it -p 5000:5000 -v $PWD:/app simple-flask-auth-app
