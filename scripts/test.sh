#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

echo "> Running tests..."
pytest --verbose --cov zoloto/ --cov-report term --cov-report html tests/

if hash black 2>/dev/null;
then
    echo "> Running formatter..."
    black zoloto tests setup.py benchmarks examples --check
fi

echo "> Running linter..."
flake8 zoloto tests setup.py benchmarks examples scripts --ignore=E128,E501,W503

echo "> Running isort..."
isort -rc -c zoloto tests setup.py benchmarks examples scripts

echo "> Running type checker..."
mypy zoloto
mypy tests
mypy benchmarks
mypy examples
mypy scripts

echo "> Running bandit..."
bandit -r zoloto/
