#!/usr/bin/env bash

set -e

python -m venv env

export PATH=env/bin:${PATH}

pip install -e ".[viewer,opencv]"
pip install -r dev-requirements.txt
