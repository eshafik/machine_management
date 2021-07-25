#!/usr/bin/env bash

readonly virtual='/home/shafik/personal/machine_management/venv/bin/activate'

source ${virtual}
python manage.py runscript clean_database_tables
python manage.py makemigrations
python manage.py migrate
python manage.py runscript enter_default_data
# python manage.py runserver
