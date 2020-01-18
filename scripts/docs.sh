#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

sphinx-build docs/ docs/_build -nWE
