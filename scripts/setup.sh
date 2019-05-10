#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

python3 -m venv env

pip install -e .
pip install -r dev-requirements.txt
