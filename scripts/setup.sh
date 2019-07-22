#!/usr/bin/env bash

set -e

poetry install

# `black` isn't available on Python3.5, so ignore if install fails
pip install black==19.3b0 || true
