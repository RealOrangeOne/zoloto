#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

rm -rf dist/*

pip install wheel

python setup.py sdist bdist_wheel
