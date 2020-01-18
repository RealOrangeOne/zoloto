#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

black zoloto tests benchmarks examples setup.py docs
isort -rc zoloto tests benchmarks examples setup.py docs
