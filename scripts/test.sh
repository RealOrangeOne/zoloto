#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

echo "> Running tests..."
pytest --cov yuri/ --cov-report term --cov-report html tests/

echo "> Running formatter..."
black yuri tests setup.py --check

echo "> Running linter..."
flake8 yuri tests setup.py --ignore=E128,E501

echo "> Running isort..."
isort -rc -c yuri tests setup.py

echo "> Running type checker..."
mypy --strict-optional --ignore-missing-imports yuri tests
