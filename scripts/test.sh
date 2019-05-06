#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

echo "> Running formatter..."
black yuri setup.py --check

echo "> Running linter..."
flake8 yuri setup.py --ignore=E128,E501

echo "> Running isort..."
isort -rc -c yuri setup.py

echo "> Running type checker..."
mypy --strict-optional --ignore-missing-imports yuri
