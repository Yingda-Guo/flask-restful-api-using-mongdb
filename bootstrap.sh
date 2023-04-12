#!/bin/sh
export ENV_FILE_LOCATION=./.env
export FLASK_APP=./app.py
pipenv run flask --debug run -h 0.0.0.0 -p 3000