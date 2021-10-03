#!/usr/bin/env bash

set -e

python3 -m venv env

export PATH=env/bin:${PATH}

pip install wheel

pip install -e "."

if [ "$1" = "opencv" ]
then
    pip install -e ".[opencv]" --prefer-binary
fi

pip install -r dev-requirements.txt
