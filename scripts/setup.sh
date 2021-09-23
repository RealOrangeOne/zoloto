#!/usr/bin/env bash

set -e

python3 -m venv env

export PATH=env/bin:${PATH}

if [ "$1" = "opencv" ]
then
    pip install -e ".[viewer,opencv]"
else
    pip install -e ".[viewer]"
fi

pip install -r dev-requirements.txt
