# app_utils_as_a_service
Utils

RUN ALL:
$ osascript tabs.scpt


Env:

## Initial Setup:
$ python3 -m venv py_env

$ source py_env/bin/activate

$ pip install --upgrade pip

$ pip install -r requirements.txt

$ django-admin startproject kfsd .

$ python ../../manage.py startapp core

## Install Pkg Locally:

$ pip install -e .