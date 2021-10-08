#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

echo "> Running tests..."
pytest -s --verbose --cov zoloto/ --cov-report term --cov-report html tests/

if hash black 2>/dev/null;
then
    echo "> Running formatter..."
    black zoloto tests benchmarks setup.py docs stubs --check
fi

echo "> Running linter..."
flake8 zoloto tests benchmarks setup.py docs stubs

echo "> Running isort..."
isort -rc -c zoloto tests benchmarks setup.py docs stubs

echo "> Running type checker..."
mypy zoloto tests docs stubs
mypy benchmarks

echo "> Running bandit..."
bandit -r zoloto/
