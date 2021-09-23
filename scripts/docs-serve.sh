#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

bash ./scripts/docs.sh

python3 -m http.server --directory docs/_build
