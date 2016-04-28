#!/bin/sh

gunicorn "api:app" --log-file=- --timeout 10 --reload
