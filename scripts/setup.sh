#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

python3 -m venv env

env/bin/pip install -e .
env/bin/pip install -r dev-requirements.txt
