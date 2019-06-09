#!/usr/bin/env bash

set -e

export PATH=env/bin:${PATH}

pytest --verbose --benchmark-sort=fullname --benchmark-columns=min,max,mean,stddev,ops benchmarks/ --benchmark-group-by=func --benchmark-name=long
