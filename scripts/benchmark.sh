#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

echo "> Running benchmarks..."
pytest --verbose --benchmark-verbose benchmarks/
