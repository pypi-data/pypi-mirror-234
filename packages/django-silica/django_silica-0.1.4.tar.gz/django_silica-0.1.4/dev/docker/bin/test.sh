#!/usr/bin/env bash

docker exec -t django-web-app python manage.py test $*
