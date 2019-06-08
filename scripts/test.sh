#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

echo "> Running tests..."
pytest --verbose --cov yuri/ --cov-report term --cov-report html tests/

if hash black 2>/dev/null;
then
    echo "> Running formatter..."
    black yuri tests setup.py benchmarks examples --check
fi

echo "> Running linter..."
flake8 yuri tests setup.py benchmarks examples --ignore=E128,E501

echo "> Running isort..."
isort -rc -c yuri tests setup.py benchmarks examples

echo "> Running type checker..."
mypy yuri
mypy tests
mypy benchmarks
mypy examples

echo "> Running bandit..."
bandit -r yuri/
