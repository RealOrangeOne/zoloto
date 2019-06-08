#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

python3 -m venv env

pip install -e .
pip install -r dev-requirements.txt

# `black` isn't available on Python3.5, so ignore if install fails
pip install black==19.3b0 || true
