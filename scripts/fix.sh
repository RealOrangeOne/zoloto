#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

black setup.py zoloto tests benchmarks examples scripts
isort -rc setup.py zoloto tests benchmarks examples scripts
