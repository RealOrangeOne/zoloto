#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

black zoloto tests benchmarks setup.py docs stubs
isort -rc zoloto tests benchmarks setup.py docs stubs
