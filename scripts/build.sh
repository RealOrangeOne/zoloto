#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

set -x

rm -rf zoloto.egg-info build/ dist/

python setup.py clean
python setup.py sdist
