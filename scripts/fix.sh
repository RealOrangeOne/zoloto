#!/usr/bin/env bash

set -e

export PATH=$(poetry show -v | grep virtualenv | sed 's/Using virtualenv: //')/bin:${PATH}

black setup.py zoloto tests benchmarks examples
isort -rc setup.py zoloto tests benchmarks examples
