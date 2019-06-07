#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

run_benchmark() {
    pytest --benchmark-sort=fullname --benchmark-name=long --benchmark-columns=min,max,mean,stddev,ops $@
}

echo "> Running calibration benchmarks..."
run_benchmark benchmarks/test_calibration.py

echo "> Running camera benchmarks..."
run_benchmark benchmarks/test_*_camera.py --benchmark-group-by=name

echo "> Running marker benchmarks..."
run_benchmark benchmarks/test_marker.py
