#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

export FLASK_APP=flask_app.py
export FLASK_ENV=development

python3 -m flask run --host=0.0.0.0
