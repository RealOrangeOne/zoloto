#!/usr/bin/env bash

set -e

export PATH=$(poetry show -v | grep virtualenv | sed 's/Using virtualenv: //')/bin:${PATH}

black zoloto tests benchmarks examples
isort -rc zoloto tests benchmarks examples
