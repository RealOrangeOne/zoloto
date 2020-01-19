#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

black zoloto tests benchmarks examples setup.py stubs
isort -rc zoloto tests benchmarks examples setup.py stubs
