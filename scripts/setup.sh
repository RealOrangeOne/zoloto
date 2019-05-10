#!/usr/bin/env bash

python3 -m venv env

env/bin/pip install -e .
env/bin/pip install -r dev-requirements.txt
