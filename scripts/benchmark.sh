#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

run_benchmark() {
    pytest --verbose --benchmark-sort=fullname --benchmark-columns=min,max,mean,stddev,ops --benchmark-group-by=func $@
}

run_benchmark benchmarks/
