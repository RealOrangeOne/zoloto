#!/usr/bin/env bash

set -e

python -m venv env

export PATH=env/bin:${PATH}

pip install -e .
pip install -r dev-requirements.txt
