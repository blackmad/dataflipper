#!/bin/bash

set -xeo pipefail

virtualenv env
./env/bin/pip install requests
./env/bin/pip install Flask

echo 'to run flipper.py, use ./env/bin/python flipper.py yourarguments'
