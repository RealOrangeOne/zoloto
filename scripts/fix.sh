#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

black setup.py yuri tests
isort -rc setup.py yuri tests
