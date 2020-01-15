#!/usr/bin/env bash

set -e

python -m venv env

export PATH=env/bin:${PATH}

pip install -e ".[viewer]"
pip install -r dev-requirements.txt
