#!/bin/sh

gunicorn "api.app:create_app()" --log-file=- --timeout 10 --reload
