#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
echo $BASEDIR
source $BASEDIR/venv/bin/activate
flask --app webapp routes
flask --app webapp run --reload --debug

 