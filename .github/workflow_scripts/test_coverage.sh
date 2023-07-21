#!/bin/bash
set -ex

source $(dirname "$0")/env_setup.sh

install_coverage_test

python3 -m pytest tests/unittests/coverage/test_coverage.py

