#!/usr/bin/env bash

set -e

export PATH=$(poetry show -v | grep virtualenv | sed 's/Using virtualenv: //')/bin:${PATH}

run_benchmark() {
    pytest --verbose --benchmark-sort=fullname --benchmark-columns=min,max,mean,stddev,ops --benchmark-group-by=func $@
}

run_benchmark benchmarks/
run_benchmark benchmarks/detection.py --benchmark-name=long
