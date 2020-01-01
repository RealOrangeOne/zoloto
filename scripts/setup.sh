#!/usr/bin/env bash

set -e

python -m venv env/

export PATH=env/bin:${PATH}

env/bin/pip install -e .
env/bin/pip install -r dev-requirements.txt
