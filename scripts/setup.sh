#!/usr/bin/env bash

set -e

python3 -m venv env

export PATH=env/bin:${PATH}

pip install wheel

if [ "$1" = "opencv" ]
then
    pip install -e ".[opencv]"
else
    pip install -e "."
fi

pip install -r dev-requirements.txt
